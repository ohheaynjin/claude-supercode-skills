# 반응 패턴 및 모범 사례

## 구성요소 패턴

### 후크가 있는 기능적 구성 요소
```typescript
import React, { useState, useEffect, useCallback, useMemo } from 'react';

interface UserCardProps {
  userId: number;
  onUpdate?: (user: User) => void;
}

export const UserCard: React.FC<UserCardProps> = ({ userId, onUpdate }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Memoize expensive computations
  const formattedName = useMemo(() => {
    return user?.name.toUpperCase() || '';
  }, [user?.name]);

  // Memoize callbacks to prevent unnecessary re-renders
  const handleUpdate = useCallback((updatedUser: User) => {
    setUser(updatedUser);
    onUpdate?.(updatedUser);
  }, [onUpdate]);

  // Data fetching
  useEffect(() => {
    let mounted = true;

    const fetchUser = async () => {
      try {
        const response = await fetch(`/api/users/${userId}`);
        const data = await response.json();
        if (mounted) {
          setUser(data);
        }
      } catch (err) {
        if (mounted) {
          setError('Failed to fetch user');
        }
      } finally {
        if (mounted) {
          setLoading(false);
        }
      }
    };

    fetchUser();

    return () => {
      mounted = false;
    };
  }, [userId]);

  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorMessage message={error} />;

  return (
    <div className="user-card">
      <h2>{formattedName}</h2>
      <UserForm user={user} onUpdate={handleUpdate} />
    </div>
  );
};
```
### 컨테이너/프레젠테이션 패턴
```typescript
// Presentational Component (dumb)
interface UserListProps {
  users: User[];
  onUserClick: (userId: number) => void;
}

export const UserList: React.FC<UserListProps> = ({ users, onUserClick }) => {
  return (
    <ul className="user-list">
      {users.map(user => (
        <li key={user.id} onClick={() => onUserClick(user.id)}>
          {user.name}
        </li>
      ))}
    </ul>
  );
};

// Container Component (smart)
export const UserListContainer: React.FC = () => {
  const { users, loading, fetchUsers } = useUsers();

  useEffect(() => {
    fetchUsers();
  }, [fetchUsers]);

  if (loading) return <LoadingSpinner />;

  return (
    <UserList
      users={users}
      onUserClick={(userId) => console.log('User clicked:', userId)}
    />
  );
};
```
### 고차 부품(HOC)
```typescript
export function withLoading<P extends object>(
  Component: React.ComponentType<P & { loading?: boolean }>
) {
  return function WithLoadingComponent(props: P & { loading?: boolean }) {
    const { loading, ...componentProps } = props;

    if (loading) {
      return <LoadingSpinner />;
    }

    return <Component {...(componentProps as P)} />;
  };
}

// Usage
const UserCardWithLoading = withLoading(UserCard);
```
### 사용자 정의 후크
```typescript
// Data fetching hook
function useFetch<T>(url: string) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let mounted = true;

    const fetchData = async () => {
      try {
        const response = await fetch(url);
        const result = await response.json();
        if (mounted) {
          setData(result);
        }
      } catch (err) {
        if (mounted) {
          setError(err instanceof Error ? err.message : 'An error occurred');
        }
      } finally {
        if (mounted) {
          setLoading(false);
        }
      }
    };

    fetchData();

    return () => {
      mounted = false;
    };
  }, [url]);

  return { data, loading, error };
}

// Form hook
function useForm<T extends Record<string, any>>(
  initialValues: T,
  validate?: (values: T) => Record<string, string>
) {
  const [values, setValues] = useState<T>(initialValues);
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [touched, setTouched] = useState<Record<string, boolean>>({});

  const handleChange = (name: keyof T) => (
    e: React.ChangeEvent<HTMLInputElement>
  ) => {
    setValues({ ...values, [name]: e.target.value });
    setTouched({ ...touched, [name]: true });
  };

  const handleSubmit = (onSubmit: (values: T) => void) => (
    e: React.FormEvent
  ) => {
    e.preventDefault();

    if (validate) {
      const validationErrors = validate(values);
      setErrors(validationErrors);

      if (Object.keys(validationErrors).length > 0) {
        return;
      }
    }

    onSubmit(values);
  };

  return {
    values,
    errors,
    touched,
    handleChange,
    handleSubmit,
  };
}
```
## 상태 관리 패턴

### 컨텍스트 API
```typescript
// Context definition
interface AuthContextType {
  user: User | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  loading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check for existing session
    const token = localStorage.getItem('token');
    if (token) {
      // Verify token and fetch user
    }
    setLoading(false);
  }, []);

  const login = async (email: string, password: string) => {
    const response = await fetch('/api/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });
    const data = await response.json();
    setUser(data.user);
    localStorage.setItem('token', data.token);
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem('token');
  };

  return (
    <AuthContext.Provider value={{ user, login, logout, loading }}>
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
## 성능 최적화

### 코드 분할
```typescript
import { lazy, Suspense } from 'react';

// Lazy load components
const Dashboard = lazy(() => import('./Dashboard'));
const Settings = lazy(() => import('./Settings'));

// Route-based code splitting
const routes = [
  {
    path: '/dashboard',
    element: (
      <Suspense fallback={<LoadingSpinner />}>
        <Dashboard />
      </Suspense>
    ),
  },
  {
    path: '/settings',
    element: (
      <Suspense fallback={<LoadingSpinner />}>
        <Settings />
      </Suspense>
    ),
  },
];
```
### 메모
```typescript
// React.memo for component memoization
export const ExpensiveComponent = React.memo(({ data }: { data: Data }) => {
  return <div>{/* expensive rendering */}</div>;
});

// useMemo for expensive computations
const filteredList = useMemo(() => {
  return list.filter(item => item.isActive);
}, [list]);

// useCallback for stable function references
const handleClick = useCallback(() => {
  console.log('Clicked');
}, []);
```
### 가상화
```typescript
import { FixedSizeList } from 'react-window';

export const VirtualList: React.FC<{ items: any[] }> = ({ items }) => {
  const Row = ({ index, style }: { index: number; style: React.CSSProperties }) => (
    <div style={style}>{items[index].name}</div>
  );

  return (
    <FixedSizeList
      height={600}
      itemCount={items.length}
      itemSize={50}
      width="100%"
    >
      {Row}
    </FixedSizeList>
  );
};
```
## 테스트 패턴

### 단위 테스트
```typescript
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { UserCard } from './UserCard';

describe('UserCard', () => {
  const mockUser = {
    id: 1,
    name: 'John Doe',
    email: 'john@example.com',
  };

  it('renders user information', () => {
    render(<UserCard user={mockUser} />);
    
    expect(screen.getByText('John Doe')).toBeInTheDocument();
    expect(screen.getByText('john@example.com')).toBeInTheDocument();
  });

  it('calls onUpdate when form is submitted', async () => {
    const onUpdate = jest.fn();
    render(<UserCard user={mockUser} onUpdate={onUpdate} />);
    
    fireEvent.click(screen.getByRole('button', { name: 'Save' }));
    
    await waitFor(() => {
      expect(onUpdate).toHaveBeenCalledWith(expect.objectContaining({
        name: 'John Doe'
      }));
    });
  });
});
```
### 통합 테스트
```typescript
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { UserList } from './UserList';

const renderWithRouter = (component: React.ReactElement) => {
  return render(
    <BrowserRouter>
      {component}
    </BrowserRouter>
  );
};

describe('UserList Integration', () => {
  it('displays users after fetching', async () => {
    renderWithRouter(<UserList />);
    
    await waitFor(() => {
      expect(screen.getByText('User 1')).toBeInTheDocument();
    });
  });

  it('navigates to user detail on click', async () => {
    renderWithRouter(<UserList />);
    
    fireEvent.click(screen.getByText('User 1'));
    
    await waitFor(() => {
      expect(window.location.pathname).toBe('/users/1');
    });
  });
});
```
## 오류 처리

### 오류 경계
```typescript
interface ErrorBoundaryState {
  hasError: boolean;
  error?: Error;
}

export class ErrorBoundary extends React.Component<
  React.PropsWithChildren<{}>,
  ErrorBoundaryState
> {
  constructor(props: React.PropsWithChildren<{}>) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error('Error caught by boundary:', error, errorInfo);
    // Log to error tracking service
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="error-boundary">
          <h2>Something went wrong</h2>
          <p>{this.state.error?.message}</p>
          <button onClick={() => window.location.reload()}>
            Reload Page
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}

// Usage
<ErrorBoundary>
  <App />
</ErrorBoundary>
```
## 양식 처리

### 제어 구성요소
```typescript
interface FormValues {
  email: string;
  password: string;
}

export const LoginForm: React.FC = () => {
  const [values, setValues] = useState<FormValues>({
    email: '',
    password: '',
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setValues({ ...values, [name]: value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    // Handle form submission
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="email"
        name="email"
        value={values.email}
        onChange={handleChange}
      />
      <input
        type="password"
        name="password"
        value={values.password}
        onChange={handleChange}
      />
      <button type="submit">Login</button>
    </form>
  );
};
```
## 접근성

### ARIA 속성
```typescript
export const AccessibleButton: React.FC<{
  children: React.ReactNode;
  onClick: () => void;
  disabled?: boolean;
}> = ({ children, onClick, disabled }) => {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      aria-disabled={disabled}
      role="button"
      tabIndex={disabled ? -1 : 0}
    >
      {children}
    </button>
  );
};
```
### 집중 관리
```typescript
export const Modal: React.FC<{ isOpen: boolean; onClose: () => void }> = ({
  isOpen,
  onClose,
}) => {
  const modalRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (isOpen && modalRef.current) {
      modalRef.current.focus();
    }
  }, [isOpen]);

  return isOpen ? (
    <div
      ref={modalRef}
      role="dialog"
      aria-modal="true"
      aria-labelledby="modal-title"
      tabIndex={-1}
    >
      <h2 id="modal-title">Modal Title</h2>
      <button onClick={onClose}>Close</button>
    </div>
  ) : null;
};
```
