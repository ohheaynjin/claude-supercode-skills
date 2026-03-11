---
name: api-designer
description: OpenAPI 3.1, HATEOAS, 페이지 매김 및 버전 관리 전략을 전문으로 하는 REST/GraphQL API 설계자
---
# API 디자이너

## 목적

OpenAPI 3.1 사양, API 버전 관리 전략, 페이지 매김 패턴 및 하이퍼미디어 기반 디자인(HATEOAS)을 전문으로 하는 전문가 REST 및 GraphQL API 아키텍처 전문 지식을 제공합니다. 적절한 오류 처리 및 표준화를 통해 확장 가능하고 잘 문서화되어 있으며 개발자 친화적인 API를 구축하는 데 중점을 둡니다.

## 사용 시기

- 요구사항에 따라 RESTful 또는 GraphQL API 설계
- API 문서화를 위한 OpenAPI 3.1 사양 생성
- API 버전 관리 전략 구현(URL, 헤더, 콘텐츠 협상)
- 대규모 데이터 세트에 대한 페이지 매김, 필터링 및 정렬 패턴 설계
- HATEOAS 호환 API 구축(하이퍼미디어 기반)
- 서비스 전반의 오류 응답 및 상태 코드 표준화
- API 인증 및 권한 부여 패턴 설계

## 빠른 시작

**다음과 같은 경우에 이 스킬을 호출하세요:**
- 요구사항에 따라 RESTful 또는 GraphQL API 설계
- API 문서화를 위한 OpenAPI 3.1 사양 생성
- API 버전 관리 전략 구현(URL, 헤더, 콘텐츠 협상)
- 대규모 데이터 세트에 대한 페이지 매김, 필터링 및 정렬 패턴 설계
- HATEOAS 호환 API 구축(하이퍼미디어 기반)
- 서비스 전반의 오류 응답 및 상태 코드 표준화

**다음과 같은 경우에는 호출하지 마세요**
- 사전 설계된 API 엔드포인트만 구현(백엔드 개발자 사용)
- API 컨텍스트 없이 데이터베이스 스키마 설계(데이터베이스 관리자 사용)
- Frontend API 통합(frontend-developer 사용)
- API 보안 구현(인증/권한 부여를 위해 보안 엔지니어 사용)
- API 성능 최적화(성능 엔지니어 사용)

---
---

## 핵심 워크플로우

### 워크플로 1: OpenAPI 3.1을 사용하여 RESTful API 설계

**사용 사례:** 전자상거래 플랫폼에는 제품 카탈로그 API가 필요합니다.

**1단계: 리소스 모델링**```yaml
# Resources identified:
# - Products (CRUD)
# - Categories (read-only, hierarchical)
# - Reviews (nested under products)
# - Inventory (separate resource, linked to products)

# URL Structure Design:
GET    /v1/products              # List products (paginated)
POST   /v1/products              # Create product
GET    /v1/products/{id}         # Get product details
PUT    /v1/products/{id}         # Update product (full replacement)
PATCH  /v1/products/{id}         # Partial update
DELETE /v1/products/{id}         # Delete product

GET    /v1/products/{id}/reviews        # Get reviews for product
POST   /v1/products/{id}/reviews        # Create review
GET    /v1/products/{id}/reviews/{reviewId}  # Get specific review

GET    /v1/categories            # List categories
GET    /v1/categories/{id}       # Get category + subcategories

# Query parameters (filtering, pagination, sorting):
GET /v1/products?category=electronics&min_price=100&max_price=500&sort=price:asc&limit=20&cursor=abc123
```

**2단계: OpenAPI 3.1 사양**```yaml
# openapi.yaml
openapi: 3.1.0
info:
  title: E-commerce Product API
  version: 1.0.0
  description: RESTful API for product catalog management
  contact:
    name: API Support
    email: api@ecommerce.com

servers:
  - url: https://api.ecommerce.com/v1
    description: Production server
  - url: https://staging-api.ecommerce.com/v1
    description: Staging server

paths:
  /products:
    get:
      summary: List products
      operationId: listProducts
      tags: [Products]
      parameters:
        - name: category
          in: query
          description: Filter by category slug
          schema:
            type: string
            example: electronics
        - name: min_price
          in: query
          description: Minimum price filter
          schema:
            type: number
            format: float
            minimum: 0
        - name: max_price
          in: query
          description: Maximum price filter
          schema:
            type: number
            format: float
            minimum: 0
        - name: sort
          in: query
          description: Sort order (field:direction)
          schema:
            type: string
            enum: [price:asc, price:desc, created_at:asc, created_at:desc]
            default: created_at:desc
        - name: limit
          in: query
          description: Number of results per page
          schema:
            type: integer
            minimum: 1
            maximum: 100
            default: 20
        - name: cursor
          in: query
          description: Pagination cursor (opaque token)
          schema:
            type: string
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                type: object
                required: [data, meta, links]
                properties:
                  data:
                    type: array
                    items:
                      $ref: '#/components/schemas/Product'
                  meta:
                    type: object
                    properties:
                      total_count:
                        type: integer
                        description: Total number of products matching filters
                      has_more:
                        type: boolean
                        description: Whether more results exist
                  links:
                    type: object
                    properties:
                      self:
                        type: string
                        format: uri
                      next:
                        type: string
                        format: uri
                        nullable: true
                      prev:
                        type: string
                        format: uri
                        nullable: true
              examples:
                success:
                  value:
                    data:
                      - id: "prod_123"
                        name: "Wireless Headphones"
                        description: "Premium noise-cancelling headphones"
                        price: 299.99
                        currency: "USD"
                        category:
                          id: "cat_1"
                          name: "Electronics"
                        created_at: "2024-01-15T10:30:00Z"
                    meta:
                      total_count: 1523
                      has_more: true
                    links:
                      self: "/v1/products?limit=20"
                      next: "/v1/products?limit=20&cursor=eyJpZCI6InByb2RfMTIzIn0="
                      prev: null
        '400':
          $ref: '#/components/responses/BadRequest'
        '500':
          $ref: '#/components/responses/InternalServerError'

  /products/{id}:
    get:
      summary: Get product details
      operationId: getProduct
      tags: [Products]
      parameters:
        - name: id
          in: path
          required: true
          description: Product ID
          schema:
            type: string
            pattern: '^prod_[a-zA-Z0-9]+$'
      responses:
        '200':
          description: Product found
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Product'
        '404':
          $ref: '#/components/responses/NotFound'

components:
  schemas:
    Product:
      type: object
      required: [id, name, price, currency]
      properties:
        id:
          type: string
          description: Unique product identifier
          example: "prod_123"
        name:
          type: string
          minLength: 1
          maxLength: 200
          example: "Wireless Headphones"
        description:
          type: string
          maxLength: 2000
          nullable: true
        price:
          type: number
          format: float
          minimum: 0
          example: 299.99
        currency:
          type: string
          enum: [USD, EUR, GBP, JPY]
          default: USD
        category:
          $ref: '#/components/schemas/Category'
        images:
          type: array
          items:
            type: string
            format: uri
          maxItems: 10
        inventory_count:
          type: integer
          minimum: 0
          description: Available stock
        created_at:
          type: string
          format: date-time
        updated_at:
          type: string
          format: date-time

    Category:
      type: object
      required: [id, name, slug]
      properties:
        id:
          type: string
          example: "cat_1"
        name:
          type: string
          example: "Electronics"
        slug:
          type: string
          pattern: '^[a-z0-9-]+$'
          example: "electronics"
        parent_id:
          type: string
          nullable: true

    Error:
      type: object
      required: [error]
      properties:
        error:
          type: object
          required: [code, message]
          properties:
            code:
              type: string
              description: Machine-readable error code
              example: "invalid_parameter"
            message:
              type: string
              description: Human-readable error message
              example: "The 'price' parameter must be a positive number"
            details:
              type: object
              description: Additional error context
              additionalProperties: true

  responses:
    BadRequest:
      description: Invalid request parameters
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            error:
              code: "invalid_parameter"
              message: "The 'min_price' parameter must be a non-negative number"
              details:
                parameter: "min_price"
                value: "-10"

    NotFound:
      description: Resource not found
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            error:
              code: "resource_not_found"
              message: "Product with ID 'prod_999' not found"

    InternalServerError:
      description: Internal server error
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            error:
              code: "internal_server_error"
              message: "An unexpected error occurred. Please try again later."
              details:
                request_id: "req_abc123"

  securitySchemes:
    ApiKey:
      type: apiKey
      in: header
      name: X-API-Key
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

security:
  - ApiKey: []
  - BearerAuth: []
```

**3단계: 문서 생성**```bash
# Install Redoc CLI
npm install -g redoc-cli

# Generate static HTML documentation
redoc-cli bundle openapi.yaml -o api-docs.html

# Host documentation
npx serve api-docs.html

# Interactive Swagger UI
docker run -p 8080:8080 -e SWAGGER_JSON=/docs/openapi.yaml \
  -v $(pwd):/docs swaggerapi/swagger-ui

# Open http://localhost:8080 for interactive API testing
```

---
---

## 안티 패턴 및 문제점

### ❌ 안티 패턴 1: 일관성 없는 오류 응답

**모습:**```json
// Endpoint 1: Login failure
{
  "error": "Invalid credentials"
}

// Endpoint 2: Validation failure
{
  "errors": [
    { "field": "email", "message": "Invalid email format" }
  ]
}

// Endpoint 3: Server error
{
  "status": "error",
  "message": "Internal server error",
  "code": 500
}

// Problem: Clients need custom error handling per endpoint
```

**실패하는 이유:**
- 클라이언트 코드가 복잡해짐(여러 오류 구문 분석 전략)
- 프론트엔드 개발자가 좌절함(일관되지 않은 계약)
- 오류 로깅/모니터링 어려움(표준 형식 없음)

**올바른 접근 방식:**```json
// Standardized error response (all endpoints)
{
  "error": {
    "code": "invalid_credentials",
    "message": "The provided email or password is incorrect",
    "details": null,
    "request_id": "req_abc123"
  }
}

// Validation errors (multiple fields)
{
  "error": {
    "code": "validation_failed",
    "message": "One or more fields failed validation",
    "details": {
      "fields": [
        { "field": "email", "message": "Invalid email format" },
        { "field": "password", "message": "Password must be at least 8 characters" }
      ]
    },
    "request_id": "req_def456"
  }
}

// Client-side error handling (consistent)
function handleApiError(response) {
  const { code, message, details } = response.error;
  
  switch (code) {
    case 'validation_failed':
      // Display field-specific errors
      details.fields.forEach(({ field, message }) => {
        showFieldError(field, message);
      });
      break;
    
    case 'unauthorized':
      // Redirect to login
      redirectToLogin();
      break;
    
    default:
      // Generic error message
      showToast(message);
  }
}
```

---
---

## 통합 패턴

**백엔드 개발자:**
- Handoff: API 디자이너가 사양 생성 → 백엔드에서 엔드포인트 구현
- 협업: 오류 대응 형식, 인증 패턴
- 도구: OpenAPI 코드 생성, API 모킹

**프런트엔드 개발자:**
- Handoff: API 사양 공개 → Frontend에서 API 사용
- 협업: 쿼리 패턴, 페이지 매김, 오류 처리
- 도구: OpenAPI/GraphQL 스키마에서 TypeScript 유형 생성

**보안 엔지니어:**
- Handoff: API 디자이너가 인증 요구 정의 → 보안이 인증 구현
- 협업: 속도 제한, API 키 관리, OAuth 흐름
- 중요: JWT 검증, API 게이트웨이 보안 정책

**개발 엔지니어:**
- Handoff: API 설계 확정 → DevOps에서 API 게이트웨이 배포
- 협업: API 버전 관리 배포, 블루-그린 릴리스
- 도구: Kong, AWS API Gateway, Traefik 구성

---
