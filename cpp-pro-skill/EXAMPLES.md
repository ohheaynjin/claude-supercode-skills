# C++ Professional - 코드 예제 및 패턴

## 잠금 없는 대기열 구현

```cpp
// Lock-free queue for high-performance scenarios
template<typename T>
class LockFreeQueue {
public:
    struct Node {
        std::atomic<Node*> next{nullptr};
        T data;
        
        template<typename... Args>
        explicit Node(Args&&... args) : data(std::forward<Args>(args)...) {}
    };

    LockFreeQueue() : dummy_(new Node{}), head_(&dummy_), tail_(&dummy_) {}
    
    ~LockFreeQueue() {
        while (Node* head = head_.load()) {
            head_.store(head->next);
            delete head;
        }
    }

    void enqueue(T value) {
        Node* new_node = new Node{std::move(value)};
        Node* prev_tail = tail_.exchange(new_node);
        prev_tail->next.store(new_node);
    }

    bool dequeue(T& result) {
        Node* head = head_.load();
        Node* next = head->next.load();
        
        if (!next) return false;
        
        result = std::move(next->data);
        head_.store(next);
        delete head;
        return true;
    }

private:
    Node* dummy_;
    std::atomic<Node*> head_;
    std::atomic<Node*> tail_;
};

using OrderQueue = LockFreeQueue<Order>;
```

## 풀 할당이 포함된 사용자 정의 스마트 포인터

```cpp
template<typename T>
class PooledPtr {
public:
    explicit PooledPtr(MemoryPool<T>& pool, T* ptr = nullptr)
        : pool_(&pool), ptr_(ptr) {}

    ~PooledPtr() {
        if (ptr_) {
            ptr_->~T();
            pool_->deallocate(ptr_, 1);
        }
    }

    PooledPtr(const PooledPtr&) = delete;
    PooledPtr& operator=(const PooledPtr&) = delete;

    PooledPtr(PooledPtr&& other) noexcept
        : pool_(other.pool_), ptr_(other.ptr_) {
        other.ptr_ = nullptr;
    }

    PooledPtr& operator=(PooledPtr&& other) noexcept {
        if (this != &other) {
            reset();
            pool_ = other.pool_;
            ptr_ = other.ptr_;
            other.ptr_ = nullptr;
        }
        return *this;
    }

    template<typename... Args>
    static PooledPtr make(MemoryPool<T>& pool, Args&&... args) {
        T* ptr = pool.allocate(1);
        new (ptr) T(std::forward<Args>(args)...);
        return PooledPtr(pool, ptr);
    }

    T& operator*() const { return *ptr_; }
    T* operator->() const { return ptr_; }
    T* get() const noexcept { return ptr_; }

    void reset() {
        if (ptr_) {
            ptr_->~T();
            pool_->deallocate(ptr_, 1);
            ptr_ = nullptr;
        }
    }

    explicit operator bool() const noexcept { return ptr_ != nullptr; }

private:
    MemoryPool<T>* pool_;
    T* ptr_;
};
```

## Google 테스트로 테스트하기

```cpp
// order_service_test.cpp
#include <gtest/gtest.h>
#include "order_service.hpp"
#include "mock_database.hpp"

using namespace order_system;

class OrderServiceTest : public ::testing::Test {
protected:
    void SetUp() override {
        mock_db_ = std::make_shared<MockDatabase>();
        service_ = std::make_unique<OrderService<MockDatabase>>(mock_db_);
    }

    std::shared_ptr<MockDatabase> mock_db_;
    std::unique_ptr<OrderService<MockDatabase>> service_;
};

TEST_F(OrderServiceTest, CreateOrder_Success) {
    // Arrange
    const std::string customer_id = "customer_123";
    const std::vector<OrderItem> items{
        {"product_1", 2, 29.99},
        {"product_2", 1, 49.99}
    };

    EXPECT_CALL(*mock_db_, insert_order(::testing::_))
        .WillOnce(::testing::Return(true));

    // Act
    auto result = service_->create_order_with_total_check(customer_id, items, 200.0);

    // Assert
    ASSERT_TRUE(result.has_value());
    EXPECT_EQ(result.value()->customer_id(), customer_id);
    EXPECT_EQ(result.value()->items().size(), 2);
    EXPECT_DOUBLE_EQ(result.value()->total_amount(), 109.97);
}

TEST_F(OrderServiceTest, CreateOrder_ExceedsMaxTotal) {
    // Arrange
    const std::string customer_id = "customer_123";
    const std::vector<OrderItem> items{
        {"product_1", 10, 100.00}
    };

    // Act
    auto result = service_->create_order_with_total_check(customer_id, items, 50.0);

    // Assert
    ASSERT_FALSE(result.has_value());
    EXPECT_STREQ(result.error().c_str(), "Order total exceeds maximum allowed amount");
}

// Property-based testing with custom generators
class OrderPropertyTest : public ::testing::Test {
protected:
    static auto generate_random_items(int count) -> std::vector<OrderItem> {
        std::vector<OrderItem> items;
        items.reserve(count);
        
        std::random_device rd;
        std::mt19937 gen(rd());
        std::uniform_int_distribution<> qty_dist(1, 10);
        std::uniform_real_distribution<> price_dist(0.01, 1000.0);

        for (int i = 0; i < count; ++i) {
            items.emplace_back(
                "product_" + std::to_string(i),
                qty_dist(gen),
                price_dist(gen)
            );
        }
        
        return items;
    }
};

TEST_F(OrderPropertyTest, TotalCalculation_Consistency) {
    for (int test = 0; test < 100; ++test) {
        const auto items = generate_random_items(10);
        
        // Test SIMD vs scalar calculation
        OrderProcessor processor;
        const double simd_total = processor.calculate_total_simd(items);
        const double scalar_total = std::accumulate(items.begin(), items.end(), 0.0,
            [](double acc, const OrderItem& item) {
                return acc + item.total();
            });

        EXPECT_DOUBLE_EQ(simd_total, scalar_total) << "Test iteration: " << test;
    }
}

// Performance benchmarks
TEST(OrderBenchmark, ParallelProcessing) {
    std::vector<Order> orders;
    orders.reserve(10000);
    
    for (int i = 0; i < 10000; ++i) {
        orders.emplace_back(
            "customer_" + std::to_string(i),
            std::vector<OrderItem>{{"product_1", 1, 29.99}}
        );
    }

    OrderProcessor processor(4);
    
    auto start = std::chrono::high_resolution_clock::now();
    processor.process_orders_parallel(orders);
    auto end = std::chrono::high_resolution_clock::now();
    
    auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);
    std::cout << "Parallel processing took: " << duration.count() << "ms\n";
    
    // Verify all orders were processed
    EXPECT_TRUE(std::all_of(orders.begin(), orders.end(),
        [](const Order& order) {
            return order.status() == OrderStatus::Completed;
        }));
}
```

## 사용 사례 예시

### 예시 1: 고성능 거래 엔진

**시나리오:** 마이크로초 수준의 응답 시간이 필요한 지연 시간이 짧은 금융 거래 엔진을 구축합니다.

**구현 접근 방식:**
1. **잠금 없는 아키텍처**: 경합이 없는 데이터 경로를 위해 원자 연산 및 메모리 순서를 사용했습니다.
2. **SIMD 최적화**: AVX-512를 사용하여 벡터화된 가격 계산을 구현했습니다.
3. **캐시 최적화**: 캐시 라인 정렬 및 프리페치를 위한 데이터 구조 설계
4. **코루틴 기반 동시성**: 효율적인 I/O 다중화를 위해 C++20 코루틴을 사용했습니다.

**성능 결과:**
- 주문 처리 지연 시간: 50μs(기존 500μs)
- 처리량: 초당 100,000개 주문(20,000개에서 증가)
- CPU 사용률: 캐시 지역성 개선을 통해 40% 감소

### 예 2: 내장형 실시간 컨트롤러

**시나리오:** 엄격한 실시간 제약 조건(< 1ms 응답)이 있는 의료 기기용 펌웨어를 개발합니다.

**구현 전략:**
1. **제로 할당 설계**: 사전 할당된 메모리 풀, 핫 경로에 동적 할당 없음
2. **constexpr Everything**: 구성 및 검증을 위한 컴파일 타임 계산
3. **개념 기반 API**: 컴파일 시 오용을 방지하는 유형 안전 인터페이스
4. **하드웨어 추상화**: 여러 마이크로컨트롤러 플랫폼을 지원하는 휴대용 레이어

**주요 기술:**```cpp
// Compile-time validated configuration
template<RealTimeSystem T>
class Controller {
    static_assert(T::max_latency_ms < 1, "Latency requirement not met");
    
    // Pre-allocated buffer pools
    std::array<Message, 256> message_pool_;
    std::atomic_size_t pool_index_{0};
};
```

### 예시 3: 크로스 플랫폼 게임 엔진 라이브러리

**시나리오:** Windows, macOS, Linux 및 콘솔로 컴파일되는 게임 엔진 SDK를 만듭니다.

**아키텍처 결정:**
1. **모듈 기반 빌드**: 더 빠른 컴파일과 깔끔한 인터페이스를 위해 C++20 모듈 사용
2. **개념 제약**: 플랫폼별 코드가 인터페이스 요구 사항을 충족하는지 확인
3. **최신 RAII**: 스마트 포인터 및 RAII 래퍼를 통한 리소스 관리
4. **오류 처리**: 예외 없이 복구 가능한 오류에 대해 std::expected 사용

**결과:**
- 컴파일 시간 단축: 모듈을 통해 45%
- 크로스 플랫폼 호환성: 95% 공유 코드
- 메모리 안전성: 2년 내 메모리 관련 CVE 제로화

## 개념 예

```cpp
// Using concepts for type-safe templates
template<typename T>
concept Serializable = requires(T t, std::ostream& os) {
    { t.serialize(os) } -> std::same_as<void>;
    { T::deserialize(std::declval<std::istream&>()) } -> std::same_as<T>;
};

template<Serializable T>
void save_to_file(const T& obj, const std::string& filename) {
    std::ofstream file(filename);
    obj.serialize(file);
}

// Compound concepts
template<typename T>
concept OrderComponent = Serializable<T> && requires(T t) {
    { t.id() } -> std::convertible_to<std::string>;
    { t.validate() } -> std::same_as<bool>;
};
```

## 범위 예

```cpp
// Modern ranges-based data processing
auto get_top_orders_by_value(const std::vector<Order>& orders, size_t n) {
    return orders
        | std::views::filter([](const Order& o) { 
            return o.status() == OrderStatus::Completed; 
        })
        | std::views::transform([](const Order& o) {
            return std::make_pair(o.id(), o.total_amount());
        })
        | std::ranges::to<std::vector>()
        | std::ranges::actions::sort([](auto& a, auto& b) {
            return a.second > b.second;
        })
        | std::views::take(n);
}

// Lazy evaluation with views
auto pending_high_value = orders
    | std::views::filter([](const Order& o) { 
        return o.status() == OrderStatus::Pending && o.total_amount() > 1000; 
    });

// Only evaluate when needed
for (const auto& order : pending_high_value | std::views::take(10)) {
    process(order);
}
```

## std::format 예

```cpp
// Type-safe formatting with std::format
std::string format_order_summary(const Order& order) {
    return std::format(
        "Order #{} | Customer: {} | Items: {} | Total: ${:.2f} | Status: {}",
        order.id(),
        order.customer_id(),
        order.items().size(),
        order.total_amount(),
        magic_enum::enum_name(order.status())
    );
}

// Format with alignment
std::string format_table_row(std::string_view name, double value) {
    return std::format("{:<20} {:>10.2f}", name, value);
}

// Format with localization
std::string format_with_locale(double amount) {
    return std::format(std::locale("en_US.UTF-8"), "{:L}", amount);
}
```
