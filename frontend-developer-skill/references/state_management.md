# 상태 관리 가이드

## 개요

올바른 상태 관리 솔루션을 선택하는 것은 애플리케이션의 복잡성, 팀 규모, 특정 사용 사례에 따라 달라집니다. 이 가이드에서는 가장 인기 있는 옵션을 다룹니다.

## Redux 툴킷

### 빠른 시작
```typescript
// store/userSlice.ts
import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';

interface UserState {
  users: User[];
  loading: boolean;
  error: string | null;
}

const initialState: UserState = {
  users: [],
  loading: false,
  error: null,
};

export const fetchUsers = createAsyncThunk(
  'users/fetchUsers',
  async () => {
    const response = await fetch('/api/users');
    return response.json();
  }
);

const userSlice = createSlice({
  name: 'users',
  initialState,
  reducers: {
    addUser: (state, action: PayloadAction<User>) => {
      state.users.push(action.payload);
    },
    updateUser: (state, action: PayloadAction<User>) => {
      const index = state.users.findIndex(u => u.id === action.payload.id);
      if (index !== -1) {
        state.users[index] = action.payload;
      }
    },
    deleteUser: (state, action: PayloadAction<number>) => {
      state.users = state.users.filter(u => u.id !== action.payload);
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchUsers.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchUsers.fulfilled, (state, action) => {
        state.loading = false;
        state.users = action.payload;
      })
      .addCase(fetchUsers.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Failed to fetch users';
      });
  },
});

export const { addUser, updateUser, deleteUser } = userSlice.actions;
export default userSlice.reducer;

// store/store.ts
import { configureStore } from '@reduxjs/toolkit';
import userReducer from './userSlice';

export const store = configureStore({
  reducer: {
    users: userReducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;

// store/hooks.ts
import { useDispatch, useSelector } from 'react-redux';
import type { RootState, AppDispatch } from './store';

export const useAppDispatch = () => useDispatch<AppDispatch>();
export const useAppSelector = <T>(selector: (state: RootState) => T): T => {
  return useSelector(selector);
};
```
### 구성요소에서의 사용법
```typescript
import { useAppDispatch, useAppSelector } from '../store/hooks';
import { fetchUsers, addUser } from '../store/userSlice';

export const UserList: React.FC = () => {
  const dispatch = useAppDispatch();
  const { users, loading, error } = useAppSelector(state => state.users);

  useEffect(() => {
    dispatch(fetchUsers());
  }, [dispatch]);

  const handleAddUser = (user: User) => {
    dispatch(addUser(user));
  };

  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorMessage message={error} />;

  return (
    <div>
      {users.map(user => (
        <UserCard key={user.id} user={user} />
      ))}
    </div>
  );
};
```
## 조건

### 기본 사용법
```typescript
// store/userStore.ts
import create from 'zustand';
import { devtools, persist } from 'zustand/middleware';

interface UserStore {
  users: User[];
  loading: boolean;
  error: string | null;
  fetchUsers: () => Promise<void>;
  addUser: (user: User) => void;
  removeUser: (id: number) => void;
}

export const useUserStore = create<UserStore>()(
  devtools(
    persist(
      (set) => ({
        users: [],
        loading: false,
        error: null,
        fetchUsers: async () => {
          set({ loading: true, error: null });
          try {
            const response = await fetch('/api/users');
            const data = await response.json();
            set({ users: data, loading: false });
          } catch (error) {
            set({
              error: error instanceof Error ? error.message : 'Failed to fetch',
              loading: false,
            });
          }
        },
        addUser: (user) => set((state) => ({ users: [...state.users, user] })),
        removeUser: (id) =>
          set((state) => ({ users: state.users.filter((u) => u.id !== id) })),
      }),
      { name: 'user-storage' }
    )
  )
);
```
### 구성요소에서의 사용법
```typescript
import { useUserStore } from '../store/userStore';

export const UserList: React.FC = () => {
  const { users, loading, error, fetchUsers, addUser } = useUserStore();

  useEffect(() => {
    fetchUsers();
  }, [fetchUsers]);

  return (
    <div>
      {users.map(user => (
        <UserCard key={user.id} user={user} />
      ))}
    </div>
  );
};
```
## 컨텍스트 API

### 설정
```typescript
// context/AuthContext.tsx
import React, { createContext, useContext, useState, useCallback } from 'react';

interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  const login = useCallback(async (email: string, password: string) => {
    const response = await fetch('/api/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });
    const data = await response.json();
    setUser(data.user);
    localStorage.setItem('token', data.token);
  }, []);

  const logout = useCallback(() => {
    setUser(null);
    localStorage.removeItem('token');
  }, []);

  return (
    <AuthContext.Provider value={{ user, loading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};
```
### 용법
```typescript
import { useAuth } from '../context/AuthContext';

export const UserProfile: React.FC = () => {
  const { user, logout } = useAuth();

  return (
    <div>
      <h1>Welcome, {user?.name}</h1>
      <button onClick={logout}>Logout</button>
    </div>
  );
};
```
## 뭔가

### 설정
```typescript
// atoms.ts
import { atom, useAtom, useSetAtom, useAtomValue } from 'jotai';
import { atomWithStorage } from 'jotai/utils';

// Primitive atom
export const countAtom = atom(0);

// Derived atom
export const doubleCountAtom = atom((get) => get(countAtom) * 2);

// Async atom
export const usersAtom = atom(async () => {
  const response = await fetch('/api/users');
  return response.json();
});

// Storage atom
export const themeAtom = atomWithStorage('theme', 'light');
```
### 용법
```typescript
import { useAtom, useAtomValue, useSetAtom } from 'jotai';
import { countAtom, doubleCountAtom, usersAtom, themeAtom } from '../atoms';

export const Counter: React.FC = () => {
  const [count, setCount] = useAtom(countAtom);
  const doubleCount = useAtomValue(doubleCountAtom);
  const setTheme = useSetAtom(themeAtom);

  return (
    <div>
      <p>Count: {count}</p>
      <p>Double: {doubleCount}</p>
      <button onClick={() => setCount(c => c + 1)}>Increment</button>
      <button onClick={() => setTheme('dark')}>Dark Mode</button>
    </div>
  );
};
```
## 반동

### 설정
```typescript
// atoms.ts
import { atom, selector, useRecoilState, useRecoilValue, useSetRecoilState } from 'recoil';

// State atom
export const countState = atom({
  key: 'countState',
  default: 0,
});

// Selector (derived state)
export const doubleCountState = selector({
  key: 'doubleCountState',
  get: ({ get }) => {
    const count = get(countState);
    return count * 2;
  },
});

// Async selector
export const usersState = selector({
  key: 'usersState',
  get: async () => {
    const response = await fetch('/api/users');
    return response.json();
  },
});
```
### 용법
```typescript
import { useRecoilState, useRecoilValue, useSetRecoilState } from 'recoil';
import { countState, doubleCountState } from '../atoms';

export const Counter: React.FC = () => {
  const [count, setCount] = useRecoilState(countState);
  const doubleCount = useRecoilValue(doubleCountState);

  return (
    <div>
      <p>Count: {count}</p>
      <p>Double: {doubleCount}</p>
      <button onClick={() => setCount(c => c + 1)}>Increment</button>
    </div>
  );
};
```
## 비교

| 기능 | 리덕스 | 주스탄 | 컨텍스트 | 조타이 | 반동 |
|---------|---------|---------|---------|-------|-------|
| 번들 크기 | 대형 | 작은 | 내장 | 작은 | 중간 |
| 학습 곡선 | 중간 | 낮음 | 낮음 | 낮음 | 중간 |
| 개발자 도구 | 우수 | 좋음 | 기본 | 좋음 | 좋음 |
| 타입스크립트 지원 | 우수 | 우수 | 좋음 | 우수 | 우수 |
| 지속성 | 예 | 예 | 매뉴얼 | 예 | 예 |
| 비동기 작업 | 내장 | 매뉴얼 | 매뉴얼 | 내장 | 내장 |
| 최고의 대상 | 대형 앱 | 모든 앱 | 작은 앱 | 모든 앱 | 대형 앱 |

## 언제 무엇을 사용해야 하는가

### Redux 툴킷
- 크고 복잡한 애플리케이션
- 고급 디버깅이 필요함
- Redux 사용 경험이 있는 팀
- 시간 이동 디버깅이 필요합니다.

### 주스탄
- 모든 크기의 적용
- 고급 기능보다 단순함을 선호합니다.
- 최소한의 상용구 필요
- TypeScript 우선 API를 원함

### 컨텍스트 API
- 중소형 애플리케이션
- 간단한 상태 요구 사항
- 외부 의존성을 피하고 싶다
- 테마, 인증, 사용자 환경 설정

### 조타이
- 모든 크기의 적용
- 원자 상태 관리를 선호합니다.
- 최소한의 상용구를 원함
- 유연한 구성이 필요함

### 반동
- 대규모 애플리케이션
- 고급 기능이 필요한 경우
- Facebook의 검증된 솔루션을 원함
- 복잡한 파생 상태 필요

## 모범 사례

### 상태를 최소로 유지
```typescript
// BAD - Store everything
const state = {
  users: [],
  userProfiles: [],
  userSettings: [],
  userPosts: [],
};

// GOOD - Store only what's needed
const state = {
  users: [],
  currentUserId: null,
};
```
### 데이터 정규화
```typescript
// BAD - Nested structures
const state = {
  users: [
    { id: 1, name: 'John', posts: [{ id: 1, title: 'Post 1' }] },
  ],
};

// GOOD - Normalized
const state = {
  users: { 1: { id: 1, name: 'John', posts: [1] } },
  posts: { 1: { id: 1, title: 'Post 1', userId: 1 } },
};
```
### 선택기 사용
```typescript
// BAD - Select in component
const users = useSelector(state => state.users);
const activeUsers = users.filter(u => u.isActive);

// GOOD - Create selector
const selectActiveUsers = createSelector(
  [state => state.users],
  users => users.filter(u => u.isActive)
);
```
