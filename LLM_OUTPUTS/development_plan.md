# The Sauce Bottle - Restructured Development Plan

## Project Overview
An app to track Australian politicians' statements and identify hypocrisy, lies, and misinformation using AI assistance. Built with Python FastAPI backend, Vue.js frontend, and LLM integration.

## Key Architecture Decisions
- **Backend**: FastAPI with SQLAlchemy and SQLite (development) / PostgreSQL (production)
- **Database Migrations**: Yoyo migrations (replaced Alembic for reliability)
- **Frontend**: Vue.js with Axios for API calls
- **AI Integration**: Direct LLM API calls (OpenAI/Anthropic/Google)
- **Development**: Incremental stages, 1-2 hours each
- **Testing**: pytest for API, manual testing for frontend

---

## PHASE 1: BACKEND FOUNDATION (Stages 1-15)

**Current Status: Stage 11 Complete** ✅  
**Next: Stage 12 - Database Session Dependencies**

**Key Improvements Made:**
- Replaced Alembic with Yoyo migrations for better reliability
- SQLite development setup eliminates Docker dependency issues
- Production-ready migration system with simple SQL approach

### Stage 1: Basic FastAPI Project Structure
- **Objective**: Set up minimal FastAPI application with proper project structure
- **Prerequisites**: Phase 0 completed (pixi, Docker, Git setup)
- **Time Estimate**: 1-2 hours
- **Deliverables**:
  - `backend/main.py` - FastAPI app entry point
  - `backend/app/__init__.py` - App package
  - `backend/app/api/__init__.py` - API package
  - Basic health check endpoint
- **Success Criteria**: FastAPI server starts and responds to `/health` endpoint
- **Key Code Components**: FastAPI app instance, basic routing

### Stage 2: Database Connection Setup
- **Objective**: Configure PostgreSQL connection with SQLAlchemy
- **Prerequisites**: Stage 1
- **Time Estimate**: 1-2 hours
- **Deliverables**:
  - `backend/app/database.py` - Database connection and session management
  - `backend/app/config.py` - Environment configuration
  - Docker Compose with PostgreSQL service
- **Success Criteria**: Database connection established, can create/drop tables
- **Key Code Components**: SQLAlchemy engine, session factory, database URL config

### Stage 3: Politician Model and Table
- **Objective**: Create Politician SQLAlchemy model and database migration
- **Prerequisites**: Stage 2
- **Time Estimate**: 1-2 hours
- **Deliverables**:
  - `backend/app/models/politician.py` - Politician SQLAlchemy model
  - `backend/app/models/__init__.py` - Models package
  - Alembic migration for Politician table
- **Success Criteria**: Politician table created in database
- **Key Code Components**: SQLAlchemy model with fields (id, name, party, position, etc.)

### Stage 4: Statement Model and Table
- **Objective**: Create Statement SQLAlchemy model with relationship to Politician
- **Prerequisites**: Stage 3
- **Time Estimate**: 1-2 hours
- **Deliverables**:
  - `backend/app/models/statement.py` - Statement SQLAlchemy model
  - Alembic migration for Statement table
  - Foreign key relationship to Politician
- **Success Criteria**: Statement table created with proper relationships
- **Key Code Components**: SQLAlchemy model with AI analysis fields (ai_summary, ai_contradiction_analysis)

### Stage 5: Pydantic Schemas
- **Objective**: Create request/response schemas for API endpoints
- **Prerequisites**: Stage 4
- **Time Estimate**: 1-2 hours
- **Deliverables**:
  - `backend/app/schemas/politician.py` - Politician schemas
  - `backend/app/schemas/statement.py` - Statement schemas
  - `backend/app/schemas/__init__.py` - Schemas package
- **Success Criteria**: Schemas validate input/output data correctly
- **Key Code Components**: BaseModel classes for create, update, response schemas

### Stage 6: Politicians CRUD Operations
- **Objective**: Implement database operations for Politicians
- **Prerequisites**: Stage 5
- **Time Estimate**: 1-2 hours
- **Deliverables**:
  - `backend/app/crud/politician.py` - CRUD functions
  - `backend/app/crud/__init__.py` - CRUD package
- **Success Criteria**: Can create, read, update, delete politicians in database
- **Key Code Components**: SQLAlchemy query functions (get, get_multi, create, update, delete)

### Stage 7: Politicians API Endpoints
- **Objective**: Create REST API endpoints for Politicians
- **Prerequisites**: Stage 6
- **Time Estimate**: 1-2 hours
- **Deliverables**:
  - `backend/app/api/endpoints/politicians.py` - API routes
  - `backend/app/api/endpoints/__init__.py` - Endpoints package
  - Integration with main FastAPI app
- **Success Criteria**: Can perform CRUD operations via HTTP requests
- **Key Code Components**: FastAPI route handlers (GET, POST, PUT, DELETE)

### Stage 8: Statements CRUD Operations
- **Objective**: Implement database operations for Statements
- **Prerequisites**: Stage 7
- **Time Estimate**: 1-2 hours
- **Deliverables**:
  - `backend/app/crud/statement.py` - Statement CRUD functions
- **Success Criteria**: Can create, read, update, delete statements with politician relationships
- **Key Code Components**: SQLAlchemy queries with joins to Politician table

### Stage 9: Statements API Endpoints
- **Objective**: Create REST API endpoints for Statements
- **Prerequisites**: Stage 8
- **Time Estimate**: 1-2 hours
- **Deliverables**:
  - `backend/app/api/endpoints/statements.py` - Statement API routes
  - Integration with FastAPI router
- **Success Criteria**: Can perform CRUD operations on statements via API
- **Key Code Components**: FastAPI route handlers with politician relationship handling

### Stage 10: API Router Integration ✅ **COMPLETED**
- **Objective**: Organize all API endpoints under a common router
- **Prerequisites**: Stage 9
- **Time Estimate**: 1 hour
- **Deliverables**:
  - ✅ `backend/app/api/api.py` - Main API router
  - ✅ Updated `main.py` to include API router
  - ✅ Migrated from Alembic to Yoyo migrations for reliability
  - ✅ SQLite development setup (no Docker dependency)
- **Success Criteria**: All endpoints accessible under `/api/v1/` prefix ✅
- **Key Code Components**: APIRouter configuration and inclusion
- **Migration System**: Yoyo migrations with SQL-based approach

### Stage 11: Basic API Error Handling ✅ **COMPLETED**
- **Objective**: Implement consistent error responses and exception handling
- **Prerequisites**: Stage 10
- **Time Estimate**: 1-2 hours
- **Deliverables**:
  - ✅ `backend/app/core/exceptions.py` - Custom exception classes
  - ✅ `backend/app/schemas/error.py` - Error response schemas
  - ✅ Error handlers in main app
  - ✅ Updated endpoints to use custom exceptions
- **Success Criteria**: API returns consistent error responses with proper HTTP status codes ✅
- **Key Code Components**: Custom exception classes, global exception handlers, structured error responses

### Stage 12: Database Session Dependencies
- **Objective**: Implement proper database session management for API endpoints
- **Prerequisites**: Stage 11
- **Time Estimate**: 1 hour
- **Deliverables**:
  - Updated `backend/app/api/deps.py` - Database session dependency
  - Updated API endpoints to use dependency injection
- **Success Criteria**: Database sessions properly created and closed for each request
- **Key Code Components**: FastAPI Depends() for database sessions

### Stage 13: Basic API Tests Setup
- **Objective**: Set up pytest with test database and basic test structure
- **Prerequisites**: Stage 12
- **Time Estimate**: 1-2 hours
- **Deliverables**:
  - `backend/tests/conftest.py` - Test configuration and fixtures
  - `backend/tests/__init__.py` - Tests package
  - `backend/tests/test_main.py` - Basic health check test
- **Success Criteria**: Can run pytest and tests pass
- **Key Code Components**: pytest fixtures for test database and client

### Stage 14: Politicians API Tests
- **Objective**: Write comprehensive tests for Politicians API endpoints
- **Prerequisites**: Stage 13
- **Time Estimate**: 1-2 hours
- **Deliverables**:
  - `backend/tests/test_politicians.py` - Politicians API tests
- **Success Criteria**: All politician CRUD operations tested and passing
- **Key Code Components**: Test functions for GET, POST, PUT, DELETE endpoints

### Stage 15: Statements API Tests
- **Objective**: Write comprehensive tests for Statements API endpoints
- **Prerequisites**: Stage 14
- **Time Estimate**: 1-2 hours
- **Deliverables**:
  - `backend/tests/test_statements.py` - Statements API tests
- **Success Criteria**: All statement CRUD operations tested and passing
- **Key Code Components**: Test functions with politician relationships

---

## PHASE 2: FRONTEND FOUNDATION (Stages 16-25)

### Stage 16: Vue.js Project Setup
- **Objective**: Initialize Vue.js project with proper structure
- **Prerequisites**: Stage 15 (Backend API working)
- **Time Estimate**: 1-2 hours
- **Deliverables**:
  - `frontend/` directory with Vue.js project
  - `frontend/src/main.js` - Vue app entry point
  - `frontend/src/App.vue` - Root component
- **Success Criteria**: Vue development server starts and displays default page
- **Key Code Components**: Vue app instance, basic component structure

### Stage 17: API Service Setup
- **Objective**: Configure Axios for API communication
- **Prerequisites**: Stage 16
- **Time Estimate**: 1 hour
- **Deliverables**:
  - `frontend/src/services/api.js` - Axios configuration
  - `frontend/src/services/politicians.js` - Politicians API calls
- **Success Criteria**: Can make API calls to backend from frontend
- **Key Code Components**: Axios instance with base URL configuration

### Stage 18: Politicians List Component
- **Objective**: Create component to display list of politicians
- **Prerequisites**: Stage 17
- **Time Estimate**: 1-2 hours
- **Deliverables**:
  - `frontend/src/components/PoliticiansList.vue` - List component
  - `frontend/src/views/Politicians.vue` - Politicians page view
- **Success Criteria**: Politicians fetched from API and displayed in list
- **Key Code Components**: Vue component with data fetching and template rendering

### Stage 19: Politician Detail Component
- **Objective**: Create component to display individual politician details
- **Prerequisites**: Stage 18
- **Time Estimate**: 1-2 hours
- **Deliverables**:
  - `frontend/src/components/PoliticianDetail.vue` - Detail component
  - `frontend/src/views/PoliticianDetail.vue` - Detail page view
- **Success Criteria**: Individual politician data displayed with statements
- **Key Code Components**: Vue component with route parameters and nested data

### Stage 20: Vue Router Setup
- **Objective**: Configure client-side routing
- **Prerequisites**: Stage 19
- **Time Estimate**: 1 hour
- **Deliverables**:
  - `frontend/src/router/index.js` - Router configuration
  - Updated `main.js` to use router
- **Success Criteria**: Navigation between politicians list and detail pages works
- **Key Code Components**: Vue Router with route definitions and navigation

### Stage 21: Statement Component
- **Objective**: Create reusable component for displaying statements
- **Prerequisites**: Stage 20
- **Time Estimate**: 1-2 hours
- **Deliverables**:
  - `frontend/src/components/StatementItem.vue` - Statement component
  - Integration with PoliticianDetail component
- **Success Criteria**: Statements displayed with proper formatting and AI analysis fields
- **Key Code Components**: Vue component with props and conditional rendering

### Stage 22: Statements API Service
- **Objective**: Add statements API calls to frontend service layer
- **Prerequisites**: Stage 21
- **Time Estimate**: 1 hour
- **Deliverables**:
  - `frontend/src/services/statements.js` - Statements API calls
  - Updated components to use statements service
- **Success Criteria**: Can fetch and display statements independently
- **Key Code Components**: Axios service functions for statements CRUD

### Stage 23: Basic Styling and Layout
- **Objective**: Add basic CSS styling and responsive layout
- **Prerequisites**: Stage 22
- **Time Estimate**: 1-2 hours
- **Deliverables**:
  - `frontend/src/assets/css/main.css` - Global styles
  - Updated components with CSS classes
  - Responsive grid layout
- **Success Criteria**: App looks presentable and works on mobile/desktop
- **Key Code Components**: CSS Grid/Flexbox layouts, component styling

### Stage 24: Navigation Component
- **Objective**: Create site navigation header/menu
- **Prerequisites**: Stage 23
- **Time Estimate**: 1 hour
- **Deliverables**:
  - `frontend/src/components/Navigation.vue` - Navigation component
  - Integration with App.vue
- **Success Criteria**: Navigation menu allows easy movement between pages
- **Key Code Components**: Vue component with router-link elements

### Stage 25: Error Handling in Frontend
- **Objective**: Implement proper error handling for API calls
- **Prerequisites**: Stage 24
- **Time Estimate**: 1-2 hours
- **Deliverables**:
  - `frontend/src/utils/errorHandler.js` - Error handling utilities
  - Updated components with error states
  - Error display components
- **Success Criteria**: API errors displayed to user gracefully
- **Key Code Components**: Try-catch blocks, error state management

---

## PHASE 3: AUTHENTICATION (Stages 26-35)

### Stage 26: User Model and Authentication Schema
- **Objective**: Create User model and authentication-related schemas
- **Prerequisites**: Stage 25
- **Time Estimate**: 1-2 hours
- **Deliverables**:
  - `backend/app/models/user.py` - User SQLAlchemy model
  - `backend/app/schemas/auth.py` - Authentication schemas
  - Alembic migration for User table
- **Success Criteria**: User table created with proper fields (username, hashed_password, etc.)
- **Key Code Components**: SQLAlchemy User model, Pydantic auth schemas

### Stage 27: Password Hashing Utilities
- **Objective**: Implement secure password hashing and verification
- **Prerequisites**: Stage 26
- **Time Estimate**: 1 hour
- **Deliverables**:
  - `backend/app/core/security.py` - Password hashing functions
  - `backend/app/core/__init__.py` - Core package
- **Success Criteria**: Can hash passwords and verify them securely
- **Key Code Components**: bcrypt or passlib for password hashing

### Stage 28: JWT Token Handling
- **Objective**: Implement JWT token creation and verification
- **Prerequisites**: Stage 27
- **Time Estimate**: 1-2 hours
- **Deliverables**:
  - Updated `backend/app/core/security.py` - JWT functions
  - `backend/app/core/config.py` - JWT configuration
- **Success Criteria**: Can create and verify JWT tokens
- **Key Code Components**: python-jose for JWT handling, token expiration

### Stage 29: User CRUD Operations
- **Objective**: Implement database operations for Users
- **Prerequisites**: Stage 28
- **Time Estimate**: 1 hour
- **Deliverables**:
  - `backend/app/crud/user.py` - User CRUD functions
- **Success Criteria**: Can create and authenticate users in database
- **Key Code Components**: SQLAlchemy user queries, password verification

### Stage 30: Authentication Endpoints
- **Objective**: Create login and user registration endpoints
- **Prerequisites**: Stage 29
- **Time Estimate**: 1-2 hours
- **Deliverables**:
  - `backend/app/api/endpoints/auth.py` - Authentication routes
  - Integration with main API router
- **Success Criteria**: Can register users and obtain JWT tokens via API
- **Key Code Components**: FastAPI OAuth2 scheme, login endpoint

### Stage 31: Authentication Dependencies
- **Objective**: Create middleware to protect API endpoints
- **Prerequisites**: Stage 30
- **Time Estimate**: 1-2 hours
- **Deliverables**:
  - Updated `backend/app/api/deps.py` - Authentication dependencies
  - Protected politician/statement endpoints
- **Success Criteria**: API endpoints require valid JWT tokens
- **Key Code Components**: FastAPI Security dependencies, current user resolution

### Stage 32: Frontend Authentication State
- **Objective**: Implement authentication state management in frontend
- **Prerequisites**: Stage 31
- **Time Estimate**: 1-2 hours
- **Deliverables**:
  - `frontend/src/stores/auth.js` - Pinia authentication store
  - `frontend/src/services/auth.js` - Authentication API calls
- **Success Criteria**: Frontend can manage authentication state
- **Key Code Components**: Pinia store with login/logout actions

### Stage 33: Login Component
- **Objective**: Create login form component
- **Prerequisites**: Stage 32
- **Time Estimate**: 1-2 hours
- **Deliverables**:
  - `frontend/src/components/LoginForm.vue` - Login form
  - `frontend/src/views/Login.vue` - Login page
- **Success Criteria**: Users can log in via frontend form
- **Key Code Components**: Vue form with validation, API integration

### Stage 34: Route Guards
- **Objective**: Protect frontend routes that require authentication
- **Prerequisites**: Stage 33
- **Time Estimate**: 1 hour
- **Deliverables**:
  - Updated `frontend/src/router/index.js` - Route guards
  - Authentication checks before route access
- **Success Criteria**: Unauthenticated users redirected to login
- **Key Code Components**: Vue Router navigation guards

### Stage 35: Authentication Testing
- **Objective**: Write tests for authentication functionality
- **Prerequisites**: Stage 34
- **Time Estimate**: 1-2 hours
- **Deliverables**:
  - `backend/tests/test_auth.py` - Authentication API tests
  - Updated API tests to include authentication
- **Success Criteria**: All authentication flows tested and working
- **Key Code Components**: Test fixtures for authenticated requests

---

## PHASE 4: AI INTEGRATION (Stages 36-50)

### Stage 36: LLM Configuration Setup
- **Objective**: Configure environment for LLM API access
- **Prerequisites**: Stage 35
- **Time Estimate**: 1 hour
- **Deliverables**:
  - Updated `backend/app/core/config.py` - LLM API configuration
  - Environment variables for API keys
  - LLM client library installation
- **Success Criteria**: LLM API credentials configured securely
- **Key Code Components**: Environment variable handling, API key management

### Stage 37: Basic LLM Service
- **Objective**: Create service layer for LLM interactions
- **Prerequisites**: Stage 36
- **Time Estimate**: 1-2 hours
- **Deliverables**:
  - `backend/app/services/__init__.py` - Services package
  - `backend/app/services/llm_service.py` - Basic LLM service
- **Success Criteria**: Can make basic API calls to chosen LLM provider
- **Key Code Components**: LLM client wrapper, basic prompt handling

### Stage 38: Statement Summarization
- **Objective**: Implement AI-powered statement summarization
- **Prerequisites**: Stage 37
- **Time Estimate**: 1-2 hours
- **Deliverables**:
  - Updated `backend/app/services/llm_service.py` - Summarization function
  - Prompts for statement summarization
- **Success Criteria**: Can generate summaries for political statements
- **Key Code Components**: LLM prompt templates, response parsing

### Stage 39: Background Task Setup
- **Objective**: Configure FastAPI background tasks for AI processing
- **Prerequisites**: Stage 38
- **Time Estimate**: 1 hour
- **Deliverables**:
  - `backend/app/core/tasks.py` - Background task functions
  - Integration with statement creation endpoints
- **Success Criteria**: AI processing happens asynchronously
- **Key Code Components**: FastAPI BackgroundTasks, async task functions

### Stage 40: AI Analysis Integration
- **Objective**: Integrate AI summarization with statement creation
- **Prerequisites**: Stage 39
- **Time Estimate**: 1-2 hours
- **Deliverables**:
  - Updated statement creation endpoints
  - AI analysis triggered on new statements
  - Database updates with AI results
- **Success Criteria**: New statements automatically get AI summaries
- **Key Code Components**: Background task integration, database updates

### Stage 41: Admin Interface for AI Results
- **Objective**: Display AI analysis results in admin interface
- **Prerequisites**: Stage 40
- **Time Estimate**: 1-2 hours
- **Deliverables**:
  - `frontend/src/components/AIAnalysis.vue` - AI results component
  - Integration with statement display components
- **Success Criteria**: AI summaries visible in frontend admin interface
- **Key Code Components**: Vue component for AI results, conditional rendering

### Stage 42: Contradiction Detection Service
- **Objective**: Implement AI-powered contradiction detection
- **Prerequisites**: Stage 41
- **Time Estimate**: 2 hours
- **Deliverables**:
  - Updated `backend/app/services/llm_service.py` - Contradiction detection
  - Prompts for comparing statements
- **Success Criteria**: Can identify potential contradictions between statements
- **Key Code Components**: Multi-statement comparison prompts, contradiction scoring

### Stage 43: Historical Statement Comparison
- **Objective**: Compare new statements against politician's history
- **Prerequisites**: Stage 42
- **Time Estimate**: 2 hours
- **Deliverables**:
  - `backend/app/services/contradiction_service.py` - Comparison service
  - Database queries for historical statements
- **Success Criteria**: New statements checked against politician's previous statements
- **Key Code Components**: Database queries, statement pairing logic

### Stage 44: Fact-Check Assistance Service
- **Objective**: Implement AI assistance for fact-checking
- **Prerequisites**: Stage 43
- **Time Estimate**: 2 hours
- **Deliverables**:
  - Updated `backend/app/services/llm_service.py` - Fact-check assistance
  - Prompts for identifying verifiable claims
- **Success Criteria**: AI can suggest fact-check approaches for statements
- **Key Code Components**: Claim extraction prompts, fact-check suggestions

### Stage 45: AI Results Review Interface
- **Objective**: Create admin interface for reviewing AI analysis
- **Prerequisites**: Stage 44
- **Time Estimate**: 2 hours
- **Deliverables**:
  - `frontend/src/views/AIReview.vue` - AI review dashboard
  - Components for approving/rejecting AI suggestions
- **Success Criteria**: Admins can review and act on AI analysis
- **Key Code Components**: Review interface, approval/rejection actions

### Stage 46: Error Handling for AI Services
- **Objective**: Implement robust error handling for LLM API calls
- **Prerequisites**: Stage 45
- **Time Estimate**: 1-2 hours
- **Deliverables**:
  - Updated AI services with try-catch blocks
  - Retry logic for failed API calls
  - Error logging and reporting
- **Success Criteria**: AI services handle API failures gracefully
- **Key Code Components**: Exception handling, retry mechanisms

### Stage 47: AI Cost Monitoring
- **Objective**: Implement monitoring for LLM API usage and costs
- **Prerequisites**: Stage 46
- **Time Estimate**: 1-2 hours
- **Deliverables**:
  - `backend/app/services/monitoring_service.py` - Usage tracking
  - Database model for API usage logs
- **Success Criteria**: Can track and monitor AI API usage costs
- **Key Code Components**: Usage logging, cost calculation

### Stage 48: Rate Limiting for AI Services
- **Objective**: Implement rate limiting to control AI API usage
- **Prerequisites**: Stage 47
- **Time Estimate**: 1 hour
- **Deliverables**:
  - Rate limiting middleware for AI services
  - Configuration for API call limits
- **Success Criteria**: AI services respect rate limits and budget constraints
- **Key Code Components**: Rate limiting logic, queue management

### Stage 49: AI Service Testing
- **Objective**: Write comprehensive tests for AI services
- **Prerequisites**: Stage 48
- **Time Estimate**: 2 hours
- **Deliverables**:
  - `backend/tests/test_ai_services.py` - AI service tests
  - Mock LLM responses for testing
- **Success Criteria**: AI services fully tested with mock responses
- **Key Code Components**: Mock API responses, service test functions

### Stage 50: AI Performance Optimization
- **Objective**: Optimize AI service performance and reliability
- **Prerequisites**: Stage 49
- **Time Estimate**: 2 hours
- **Deliverables**:
  - Optimized prompts for better results
  - Caching for repeated AI requests
  - Performance metrics collection
- **Success Criteria**: AI services perform efficiently with good results
- **Key Code Components**: Prompt optimization, caching layer

---

## Next Phases Preview

**Phase 5: Web Scraping (Stages 51-65)**
- Web scraper development
- Content extraction and processing
- Integration with AI analysis
- Automated content ingestion

**Phase 6: Deployment & Production (Stages 66-80)**
- Docker production configuration
- AWS deployment setup
- CI/CD pipeline implementation
- Production monitoring

**Phase 7: Advanced Features (Stages 81+)**
- Semantic search implementation
- Advanced AI agents
- User features and notifications
- Performance optimization

---

## Development Guidelines

### Testing Strategy
- Write tests for each stage before moving to next
- Use pytest fixtures for database and API testing
- Mock external services (LLM APIs) in tests
- Maintain test coverage above 80%

### Code Quality
- Use type hints throughout Python code
- Follow PEP 8 style guidelines
- Use ruff for linting and formatting
- Document functions and classes

### Git Workflow
- Create feature branch for each stage
- Commit frequently with descriptive messages
- Merge to main after stage completion and testing
- Tag releases at phase completions

### Error Handling
- Implement proper exception handling
- Log errors appropriately
- Provide meaningful error messages to users
- Handle edge cases and validation errors

### Security Considerations
- Never commit API keys or secrets
- Use environment variables for configuration
- Implement proper authentication and authorization
- Validate all user inputs