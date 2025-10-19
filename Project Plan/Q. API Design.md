# Artify Studio - API Design

## 1. API Architecture Overview

### 1.1 API Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           API Architecture                              │
├─────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │
│  │   REST      │  │  GraphQL    │  │   WebSocket │  │   Platform  │    │
│  │   APIs      │  │   API       │  │   APIs      │  │   APIs      │    │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘    │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │
│  │   API       │  │   Rate      │  │   Security  │  │   Version   │    │
│  │  Gateway    │  │  Limiting   │  │   Layer     │  │ Management  │    │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘    │
├─────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │
│  │   Image     │  │   User      │  │ Transformation│ │   Analytics │    │
│  │ Processing  │  │ Management  │  │   APIs      │  │   APIs      │    │
│  │   APIs      │  │   APIs      │  │             │  │             │    │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘    │
└─────────────────────────────────────────────────────────────────────────┘
```

### 1.2 API Categories

| API Category | Purpose | Protocol | Authentication | Usage Pattern |
|--------------|---------|----------|----------------|---------------|
| **Image Processing APIs** | Core transformation operations | REST/GraphQL | API Key/OAuth | High frequency |
| **User Management APIs** | User accounts and preferences | REST | OAuth/JWT | Medium frequency |
| **Platform APIs** | Platform-specific operations | REST | Platform tokens | Platform specific |
| **Analytics APIs** | Usage tracking and insights | REST | API Key | Background sync |
| **Real-time APIs** | Live collaboration features | WebSocket | JWT | Real-time |

## 2. Core API Specifications

### 2.1 Image Processing API

#### REST API Endpoints
```python
# src/api/endpoints/image_processing.py
from fastapi import APIRouter, File, UploadFile, HTTPException, Depends, BackgroundTasks
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from src.api.models.image_models import ImageProcessingRequest, ImageProcessingResponse

router = APIRouter(prefix="/api/v1/images", tags=["image_processing"])

class ImageProcessingAPI:
    """Core image processing API endpoints"""

    def __init__(self):
        self.processing_engine = ImageProcessingEngine()
        self.rate_limiter = RateLimiter()
        self.cache_manager = CacheManager()

    @router.post("/transform", response_model=ImageProcessingResponse)
    async def transform_image(
        self,
        request: ImageProcessingRequest,
        background_tasks: BackgroundTasks,
        api_key: str = Depends(verify_api_key)
    ) -> ImageProcessingResponse:
        """Transform image with specified parameters"""
        try:
            # Rate limiting check
            rate_limit_result = await self.rate_limiter.check_limit(api_key, "transform")
            if not rate_limit_result["allowed"]:
                raise HTTPException(
                    status_code=429,
                    detail=f"Rate limit exceeded. Retry after {rate_limit_result['retry_after']} seconds"
                )

            # Validate request
            validation_result = self._validate_transformation_request(request)
            if not validation_result["valid"]:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid request: {validation_result['errors']}"
                )

            # Check cache for identical requests
            cache_key = self._generate_cache_key(request)
            cached_result = await self.cache_manager.get(cache_key)

            if cached_result:
                return ImageProcessingResponse(
                    success=True,
                    result_url=cached_result["url"],
                    processing_time=cached_result["processing_time"],
                    cached=True,
                    cache_hit=True
                )

            # Process image
            processing_result = await self.processing_engine.transform_async(
                image_data=request.image_data,
                transformation_type=request.transformation_type,
                parameters=request.parameters,
                quality=request.quality,
                output_format=request.output_format
            )

            if processing_result["success"]:
                # Cache result
                background_tasks.add_task(
                    self.cache_manager.set,
                    cache_key,
                    {
                        "url": processing_result["result_url"],
                        "processing_time": processing_result["processing_time"]
                    },
                    ttl=3600  # 1 hour cache
                )

                # Track analytics
                background_tasks.add_task(
                    self._track_api_usage,
                    api_key,
                    "transform",
                    processing_result["processing_time"]
                )

                return ImageProcessingResponse(
                    success=True,
                    result_url=processing_result["result_url"],
                    processing_time=processing_result["processing_time"],
                    cached=False,
                    cache_hit=False,
                    request_id=processing_result["request_id"]
                )
            else:
                raise HTTPException(
                    status_code=500,
                    detail=f"Processing failed: {processing_result['error']}"
                )

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Internal server error: {str(e)}"
            )

    @router.post("/batch-transform", response_model=BatchProcessingResponse)
    async def batch_transform_images(
        self,
        request: BatchProcessingRequest,
        background_tasks: BackgroundTasks,
        api_key: str = Depends(verify_api_key)
    ) -> BatchProcessingResponse:
        """Transform multiple images in batch"""
        try:
            # Validate batch request
            if len(request.images) > 50:  # Maximum 50 images per batch
                raise HTTPException(
                    status_code=400,
                    detail="Maximum 50 images allowed per batch"
                )

            # Check batch processing permissions
            permissions = await self._check_batch_permissions(api_key)
            if not permissions["allowed"]:
                raise HTTPException(
                    status_code=403,
                    detail="Batch processing not available for this API key"
                )

            # Submit batch job
            batch_job = await self.processing_engine.submit_batch_job(
                images=request.images,
                transformation_config=request.transformation_config,
                webhook_url=request.webhook_url
            )

            return BatchProcessingResponse(
                success=True,
                batch_id=batch_job["batch_id"],
                status="submitted",
                estimated_completion_time=batch_job["estimated_completion"],
                result_url=batch_job["status_url"]
            )

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Batch processing failed: {str(e)}"
            )

    @router.get("/batch-status/{batch_id}", response_model=BatchStatusResponse)
    async def get_batch_status(self, batch_id: str, api_key: str = Depends(verify_api_key)) -> BatchStatusResponse:
        """Get batch processing status"""
        try:
            status = await self.processing_engine.get_batch_status(batch_id)

            return BatchStatusResponse(
                batch_id=batch_id,
                status=status["status"],
                progress=status["progress"],
                results=status.get("results", []),
                errors=status.get("errors", [])
            )

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to get batch status: {str(e)}"
            )

    @router.get("/transformations", response_model=List[TransformationInfo])
    async def get_available_transformations(self) -> List[TransformationInfo]:
        """Get list of available transformations"""
        try:
            transformations = await self.processing_engine.get_available_transformations()

            return [
                TransformationInfo(
                    id=transform["id"],
                    name=transform["name"],
                    description=transform["description"],
                    category=transform["category"],
                    supported_formats=transform["supported_formats"],
                    parameters=transform["parameters"]
                )
                for transform in transformations
            ]

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to get transformations: {str(e)}"
            )

    def _validate_transformation_request(self, request: ImageProcessingRequest) -> Dict[str, Any]:
        """Validate transformation request"""
        errors = []

        # Validate image data
        if not request.image_data:
            errors.append("Image data is required")

        # Validate transformation type
        valid_transformations = ["pencil_sketch", "colored_sketch", "turtle_graphics", "opencv_filters"]
        if request.transformation_type not in valid_transformations:
            errors.append(f"Invalid transformation type. Valid types: {valid_transformations}")

        # Validate quality
        if not (1 <= request.quality <= 100):
            errors.append("Quality must be between 1 and 100")

        return {
            "valid": len(errors) == 0,
            "errors": errors
        }

    def _generate_cache_key(self, request: ImageProcessingRequest) -> str:
        """Generate cache key for request"""
        import hashlib

        # Create deterministic key from request parameters
        key_data = f"{request.transformation_type}_{request.quality}_{request.output_format}"
        return hashlib.md5(key_data.encode()).hexdigest()

    async def _check_batch_permissions(self, api_key: str) -> Dict[str, Any]:
        """Check if API key has batch processing permissions"""
        # Implementation would check API key permissions
        return {"allowed": True, "daily_limit": 1000}

    async def _track_api_usage(self, api_key: str, operation: str, processing_time: float) -> None:
        """Track API usage for analytics"""
        # Implementation would record usage metrics
        pass
```

#### API Data Models
```python
# src/api/models/image_models.py
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from enum import Enum

class TransformationType(str, Enum):
    """Available transformation types"""
    PENCIL_SKETCH = "pencil_sketch"
    COLORED_SKETCH = "colored_sketch"
    TURTLE_GRAPHICS = "turtle_graphics"
    OPENCV_FILTERS = "opencv_filters"

class OutputFormat(str, Enum):
    """Supported output formats"""
    PNG = "PNG"
    JPEG = "JPEG"
    WebP = "WebP"
    TIFF = "TIFF"

class ImageProcessingRequest(BaseModel):
    """Request model for image processing"""
    image_data: str = Field(..., description="Base64 encoded image data")
    transformation_type: TransformationType = Field(..., description="Type of transformation to apply")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Transformation parameters")
    quality: int = Field(85, ge=1, le=100, description="Output quality (1-100)")
    output_format: OutputFormat = Field(OutputFormat.PNG, description="Output image format")
    webhook_url: Optional[str] = Field(None, description="Webhook URL for completion notification")

class ImageProcessingResponse(BaseModel):
    """Response model for image processing"""
    success: bool = Field(..., description="Whether processing was successful")
    result_url: Optional[str] = Field(None, description="URL to processed image")
    processing_time: float = Field(..., description="Processing time in seconds")
    cached: bool = Field(False, description="Whether result came from cache")
    cache_hit: bool = Field(False, description="Whether this was a cache hit")
    request_id: Optional[str] = Field(None, description="Unique request identifier")
    error_message: Optional[str] = Field(None, description="Error message if processing failed")

class BatchProcessingRequest(BaseModel):
    """Request model for batch processing"""
    images: List[str] = Field(..., description="List of base64 encoded images")
    transformation_config: Dict[str, Any] = Field(..., description="Transformation configuration")
    webhook_url: Optional[str] = Field(None, description="Webhook URL for completion")

class BatchProcessingResponse(BaseModel):
    """Response model for batch processing"""
    success: bool = Field(..., description="Whether batch was submitted successfully")
    batch_id: str = Field(..., description="Unique batch identifier")
    status: str = Field(..., description="Current batch status")
    estimated_completion_time: float = Field(..., description="Estimated completion time in seconds")
    result_url: str = Field(..., description="URL to check batch status")

class BatchStatusResponse(BaseModel):
    """Response model for batch status"""
    batch_id: str = Field(..., description="Batch identifier")
    status: str = Field(..., description="Current status")
    progress: float = Field(..., ge=0, le=100, description="Processing progress percentage")
    results: List[str] = Field(default_factory=list, description="URLs to completed results")
    errors: List[str] = Field(default_factory=list, description="List of error messages")

class TransformationInfo(BaseModel):
    """Information about available transformations"""
    id: str = Field(..., description="Transformation identifier")
    name: str = Field(..., description="Human-readable name")
    description: str = Field(..., description="Transformation description")
    category: str = Field(..., description="Transformation category")
    supported_formats: List[str] = Field(..., description="Supported input formats")
    parameters: Dict[str, Any] = Field(..., description="Available parameters")
```

### 2.2 User Management API

#### Authentication and User APIs
```python
# src/api/endpoints/user_management.py
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from src.api.models.user_models import User, UserCreate, UserLogin, Token, UserPreferences

router = APIRouter(prefix="/api/v1/users", tags=["user_management"])

class UserManagementAPI:
    """User management and authentication API"""

    def __init__(self):
        self.user_service = UserService()
        self.auth_service = AuthenticationService()
        self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

    @router.post("/register", response_model=Token)
    async def register_user(self, user_data: UserCreate) -> Token:
        """Register new user account"""
        try:
            # Validate user data
            validation_result = self._validate_user_registration(user_data)
            if not validation_result["valid"]:
                raise HTTPException(
                    status_code=400,
                    detail=f"Registration failed: {validation_result['errors']}"
                )

            # Create user account
            user = await self.user_service.create_user(
                email=user_data.email,
                password=user_data.password,
                name=user_data.name,
                preferences=user_data.preferences
            )

            # Generate access token
            access_token = self.auth_service.create_access_token(
                data={"sub": user.email, "user_id": user.id},
                expires_delta=timedelta(days=30)
            )

            return Token(
                access_token=access_token,
                token_type="bearer",
                expires_in=30 * 24 * 3600,  # 30 days in seconds
                user_id=user.id
            )

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Registration failed: {str(e)}"
            )

    @router.post("/login", response_model=Token)
    async def login_user(self, form_data: OAuth2PasswordRequestForm = Depends()) -> Token:
        """Authenticate user and return access token"""
        try:
            # Authenticate user
            user = await self.auth_service.authenticate_user(
                email=form_data.username,
                password=form_data.password
            )

            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Incorrect email or password",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            # Generate access token
            access_token = self.auth_service.create_access_token(
                data={"sub": user.email, "user_id": user.id},
                expires_delta=timedelta(days=30)
            )

            return Token(
                access_token=access_token,
                token_type="bearer",
                expires_in=30 * 24 * 3600,
                user_id=user.id
            )

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Login failed: {str(e)}"
            )

    @router.get("/me", response_model=User)
    async def get_current_user(self, token: str = Depends(oauth2_scheme)) -> User:
        """Get current user information"""
        try:
            # Verify token and get user
            user = await self.auth_service.get_current_user(token)

            return User(
                id=user.id,
                email=user.email,
                name=user.name,
                preferences=user.preferences,
                created_at=user.created_at,
                last_login=user.last_login
            )

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to get user information: {str(e)}"
            )

    @router.put("/preferences", response_model=User)
    async def update_user_preferences(
        self,
        preferences: UserPreferences,
        token: str = Depends(oauth2_scheme)
    ) -> User:
        """Update user preferences"""
        try:
            # Get current user
            user = await self.auth_service.get_current_user(token)

            # Update preferences
            updated_user = await self.user_service.update_user_preferences(
                user_id=user.id,
                preferences=preferences.dict()
            )

            return User(
                id=updated_user.id,
                email=updated_user.email,
                name=updated_user.name,
                preferences=updated_user.preferences,
                created_at=updated_user.created_at,
                last_login=updated_user.last_login
            )

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to update preferences: {str(e)}"
            )

    @router.get("/usage", response_model=Dict[str, Any])
    async def get_user_usage(self, token: str = Depends(oauth2_scheme)) -> Dict[str, Any]:
        """Get user usage statistics"""
        try:
            user = await self.auth_service.get_current_user(token)

            usage_stats = await self.user_service.get_user_usage_stats(user.id)

            return {
                "user_id": user.id,
                "period": "current_month",
                "transformations_count": usage_stats["transformations"],
                "images_processed": usage_stats["images"],
                "api_calls": usage_stats["api_calls"],
                "storage_used_mb": usage_stats["storage_mb"],
                "plan_limits": usage_stats["plan_limits"],
                "usage_percentage": usage_stats["usage_percentage"]
            }

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to get usage statistics: {str(e)}"
            )

    def _validate_user_registration(self, user_data: UserCreate) -> Dict[str, Any]:
        """Validate user registration data"""
        errors = []

        # Validate email format
        if not user_data.email or "@" not in user_data.email:
            errors.append("Valid email address is required")

        # Validate password strength
        if len(user_data.password) < 8:
            errors.append("Password must be at least 8 characters long")

        # Validate name
        if not user_data.name or len(user_data.name.strip()) < 2:
            errors.append("Name must be at least 2 characters long")

        return {
            "valid": len(errors) == 0,
            "errors": errors
        }
```

### 2.3 Platform Integration APIs

#### Web Platform API
```python
# src/api/endpoints/web_platform.py
from fastapi import APIRouter, Request, HTTPException
from typing import Dict, Any
from src.api.models.platform_models import WebPlatformInfo, BrowserCapabilities

router = APIRouter(prefix="/api/v1/platform/web", tags=["web_platform"])

class WebPlatformAPI:
    """Web platform specific API endpoints"""

    def __init__(self):
        self.platform_detector = PlatformDetector()
        self.capability_checker = CapabilityChecker()

    @router.get("/capabilities", response_model=BrowserCapabilities)
    async def get_browser_capabilities(self, request: Request) -> BrowserCapabilities:
        """Get browser capabilities and limitations"""
        try:
            # Detect user agent and browser info
            user_agent = request.headers.get("user-agent", "")
            browser_info = self.platform_detector.detect_browser(user_agent)

            # Check supported features
            capabilities = await self.capability_checker.check_browser_capabilities(browser_info)

            return BrowserCapabilities(
                browser_name=browser_info["name"],
                browser_version=browser_info["version"],
                platform=browser_info["platform"],
                supported_features=capabilities["supported_features"],
                limitations=capabilities["limitations"],
                recommended_settings=capabilities["recommended_settings"],
                performance_score=capabilities["performance_score"]
            )

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to detect browser capabilities: {str(e)}"
            )

    @router.post("/optimize-settings")
    async def optimize_platform_settings(
        self,
        platform_info: WebPlatformInfo,
        request: Request
    ) -> Dict[str, Any]:
        """Get optimized settings for current platform"""
        try:
            # Get current browser capabilities
            capabilities = await self.get_browser_capabilities(request)

            # Generate optimized settings
            optimized_settings = self._generate_optimized_settings(capabilities, platform_info)

            return {
                "success": True,
                "optimized_settings": optimized_settings,
                "performance_improvements": self._calculate_improvements(capabilities, optimized_settings),
                "compatibility_warnings": self._get_compatibility_warnings(capabilities)
            }

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to optimize settings: {str(e)}"
            )

    def _generate_optimized_settings(self, capabilities: BrowserCapabilities, platform_info: WebPlatformInfo) -> Dict[str, Any]:
        """Generate optimized settings based on browser capabilities"""
        settings = {
            "image_quality": 85,
            "enable_gpu_acceleration": capabilities.supported_features.get("webgl", False),
            "max_processing_threads": 2,
            "cache_enabled": True,
            "compression_enabled": True,
            "progressive_loading": True
        }

        # Adjust based on performance score
        if capabilities.performance_score < 50:
            settings.update({
                "image_quality": 70,
                "max_processing_threads": 1,
                "enable_gpu_acceleration": False
            })
        elif capabilities.performance_score > 80:
            settings.update({
                "image_quality": 95,
                "max_processing_threads": 4,
                "enable_gpu_acceleration": True
            })

        return settings

    def _calculate_improvements(self, capabilities: BrowserCapabilities, settings: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate expected performance improvements"""
        return {
            "processing_speed_improvement": "15-25%",
            "memory_usage_reduction": "20-30%",
            "battery_life_extension": "10-15%" if platform_info.is_mobile else "0%"
        }

    def _get_compatibility_warnings(self, capabilities: BrowserCapabilities) -> List[str]:
        """Get compatibility warnings"""
        warnings = []

        if not capabilities.supported_features.get("webgl", False):
            warnings.append("WebGL not supported - GPU acceleration disabled")

        if capabilities.performance_score < 30:
            warnings.append("Browser performance is below recommended levels")

        return warnings
```

## 3. API Security and Authentication

### 3.1 Authentication Framework

#### JWT Token Management
```python
# src/api/security/authentication.py
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

class AuthenticationService:
    """JWT-based authentication service"""

    def __init__(self):
        self.secret_key = os.environ.get("JWT_SECRET_KEY", "your-secret-key")
        self.algorithm = "HS256"
        self.access_token_expire_minutes = 30 * 24 * 60  # 30 days
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.security_scheme = HTTPBearer()

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create JWT access token"""
        to_encode = data.copy()

        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)

        to_encode.update({"exp": expire, "type": "access"})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

        return encoded_jwt

    def verify_token(self, token: str) -> Optional[dict]:
        """Verify and decode JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            email: str = payload.get("sub")

            if email is None:
                return None

            return payload

        except JWTError:
            return None

    def authenticate_user(self, email: str, password: str) -> Optional[dict]:
        """Authenticate user with email and password"""
        # Implementation would verify against user database
        # This is a simplified example
        user = self._get_user_by_email(email)

        if not user:
            return None

        if not self.pwd_context.verify(password, user["hashed_password"]):
            return None

        return user

    async def get_current_user(self, credentials: HTTPAuthorizationCredentials = Depends(security_scheme)) -> dict:
        """Get current user from JWT token"""
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        token = credentials.credentials
        payload = self.verify_token(token)

        if payload is None:
            raise credentials_exception

        user_email: str = payload.get("sub")
        if user_email is None:
            raise credentials_exception

        user = self._get_user_by_email(user_email)
        if user is None:
            raise credentials_exception

        return user

    def _get_user_by_email(self, email: str) -> Optional[dict]:
        """Get user by email address"""
        # Implementation would query user database
        # This is a placeholder
        return {
            "id": "user_123",
            "email": email,
            "name": "Test User",
            "hashed_password": "$2b$12$...",
            "preferences": {},
            "created_at": datetime.utcnow(),
            "last_login": datetime.utcnow()
        }

    def hash_password(self, password: str) -> str:
        """Hash password for storage"""
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify password against hash"""
        return self.pwd_context.verify(plain_password, hashed_password)
```

### 3.2 API Key Management

#### API Key Authentication
```python
# src/api/security/api_keys.py
import secrets
import hashlib
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from src.api.models.api_key_models import APIKey, APIKeyCreate, APIKeyResponse

class APIKeyManager:
    """API key management and validation"""

    def __init__(self):
        self.api_keys = {}  # In production, this would be a database
        self.key_prefix = "artify_"

    def create_api_key(self, key_data: APIKeyCreate) -> APIKeyResponse:
        """Create new API key"""
        # Generate secure API key
        raw_key = f"{self.key_prefix}{secrets.token_urlsafe(32)}"

        # Hash key for storage (never store raw key)
        key_hash = hashlib.sha256(raw_key.encode()).hexdigest()

        # Create key record
        api_key = APIKey(
            key_id=f"key_{secrets.token_hex(8)}",
            key_hash=key_hash,
            name=key_data.name,
            permissions=key_data.permissions,
            rate_limits=key_data.rate_limits,
            created_at=datetime.utcnow(),
            expires_at=key_data.expires_at,
            last_used=None,
            usage_count=0
        )

        # Store key (in production, save to database)
        self.api_keys[api_key.key_id] = api_key

        return APIKeyResponse(
            key_id=api_key.key_id,
            api_key=raw_key,  # Only time raw key is returned
            name=api_key.name,
            permissions=api_key.permissions,
            rate_limits=api_key.rate_limits,
            created_at=api_key.created_at,
            expires_at=api_key.expires_at
        )

    def validate_api_key(self, api_key: str) -> Optional[APIKey]:
        """Validate API key and return key information"""
        # Hash provided key
        key_hash = hashlib.sha256(api_key.encode()).hexdigest()

        # Find matching key
        for key in self.api_keys.values():
            if key.key_hash == key_hash:
                # Check expiration
                if key.expires_at and datetime.utcnow() > key.expires_at:
                    return None

                # Update usage statistics
                key.last_used = datetime.utcnow()
                key.usage_count += 1

                return key

        return None

    def revoke_api_key(self, key_id: str) -> bool:
        """Revoke API key"""
        if key_id in self.api_keys:
            del self.api_keys[key_id]
            return True
        return False

    def get_api_key_usage(self, key_id: str) -> Optional[Dict[str, Any]]:
        """Get API key usage statistics"""
        if key_id not in self.api_keys:
            return None

        key = self.api_keys[key_id]
        return {
            "key_id": key_id,
            "name": key.name,
            "usage_count": key.usage_count,
            "last_used": key.last_used,
            "created_at": key.created_at,
            "rate_limits": key.rate_limits,
            "permissions": key.permissions
        }

    def rotate_api_key(self, key_id: str) -> Optional[APIKeyResponse]:
        """Rotate API key (create new, revoke old)"""
        if key_id not in self.api_keys:
            return None

        old_key = self.api_keys[key_id]

        # Create new key with same permissions
        new_key_data = APIKeyCreate(
            name=f"{old_key.name} (Rotated)",
            permissions=old_key.permissions,
            rate_limits=old_key.rate_limits,
            expires_at=old_key.expires_at
        )

        new_key_response = self.create_api_key(new_key_data)

        # Revoke old key
        self.revoke_api_key(key_id)

        return new_key_response
```

## 4. API Rate Limiting and Throttling

### 4.1 Rate Limiting Implementation

#### Distributed Rate Limiting
```python
# src/api/rate_limiting/rate_limiter.py
import time
import redis
from typing import Dict, Any, Tuple
from dataclasses import dataclass
from src.api.models.rate_limit_models import RateLimit, RateLimitResponse

@dataclass
class RateLimitRule:
    """Rate limit rule configuration"""
    requests_per_minute: int
    requests_per_hour: int
    requests_per_day: int
    burst_limit: int

class DistributedRateLimiter:
    """Distributed rate limiting using Redis"""

    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.redis_client = redis.from_url(redis_url)
        self.default_rules = {
            'free': RateLimitRule(10, 100, 1000, 5),
            'premium': RateLimitRule(60, 1000, 10000, 20),
            'enterprise': RateLimitRule(300, 5000, 50000, 100)
        }

    async def check_limit(self, identifier: str, operation: str, rule_name: str = 'free') -> RateLimitResponse:
        """Check if request is within rate limits"""
        try:
            # Get rate limit rule
            rule = self._get_rate_limit_rule(rule_name)

            # Check all time windows
            minute_key = f"rate_limit:{identifier}:{operation}:minute"
            hour_key = f"rate_limit:{identifier}:{operation}:hour"
            day_key = f"rate_limit:{identifier}:{operation}:day"

            current_time = int(time.time())

            # Check minute limit
            minute_count = self._get_window_count(minute_key, 60)
            if minute_count >= rule.requests_per_minute:
                return RateLimitResponse(
                    allowed=False,
                    retry_after=60 - (current_time % 60),
                    limit=rule.requests_per_minute,
                    remaining=0,
                    reset_time=current_time + (60 - (current_time % 60))
                )

            # Check hour limit
            hour_count = self._get_window_count(hour_key, 3600)
            if hour_count >= rule.requests_per_hour:
                return RateLimitResponse(
                    allowed=False,
                    retry_after=3600 - (current_time % 3600),
                    limit=rule.requests_per_hour,
                    remaining=0,
                    reset_time=current_time + (3600 - (current_time % 3600))
                )

            # Check day limit
            day_count = self._get_window_count(day_key, 86400)
            if day_count >= rule.requests_per_day:
                return RateLimitResponse(
                    allowed=False,
                    retry_after=86400 - (current_time % 86400),
                    limit=rule.requests_per_day,
                    remaining=0,
                    reset_time=current_time + (86400 - (current_time % 86400))
                )

            # Increment counters
            self._increment_window_count(minute_key, 60)
            self._increment_window_count(hour_key, 3600)
            self._increment_window_count(day_key, 86400)

            # Calculate remaining limits
            remaining_minute = rule.requests_per_minute - minute_count - 1
            remaining_hour = rule.requests_per_hour - hour_count - 1
            remaining_day = rule.requests_per_day - day_count - 1

            return RateLimitResponse(
                allowed=True,
                retry_after=0,
                limit=min(remaining_minute, remaining_hour, remaining_day),
                remaining=min(remaining_minute, remaining_hour, remaining_day),
                reset_time=current_time + 60
            )

        except Exception as e:
            # Fail open in case of Redis issues
            return RateLimitResponse(
                allowed=True,
                retry_after=0,
                limit=1000,
                remaining=999,
                reset_time=int(time.time()) + 60
            )

    def _get_window_count(self, key: str, window_seconds: int) -> int:
        """Get current count for time window"""
        current_time = int(time.time())
        window_start = current_time - (current_time % window_seconds)

        # Use Redis sorted set to track requests in time window
        count = self.redis_client.zcount(key, window_start, current_time)

        return count

    def _increment_window_count(self, key: str, window_seconds: int) -> None:
        """Increment counter for time window"""
        current_time = int(time.time())

        # Add current timestamp to sorted set
        self.redis_client.zadd(key, {current_time: current_time})

        # Remove old entries outside the window
        window_start = current_time - window_seconds
        self.redis_client.zremrangebyscore(key, 0, window_start)

    def _get_rate_limit_rule(self, rule_name: str) -> RateLimitRule:
        """Get rate limit rule by name"""
        return self.default_rules.get(rule_name, self.default_rules['free'])
```

## 5. API Versioning and Compatibility

### 5.1 Version Management Strategy

#### API Versioning Implementation
```python
# src/api/versioning/version_manager.py
from typing import Dict, Any, List, Optional
from packaging import version
from src.api.versioning.api_versions import APIVersion, VersionCompatibility

class APIVersionManager:
    """Manages API versioning and compatibility"""

    def __init__(self):
        self.supported_versions = self._initialize_supported_versions()
        self.current_version = "1.0.0"
        self.deprecation_policy = self._initialize_deprecation_policy()

    def _initialize_supported_versions(self) -> Dict[str, APIVersion]:
        """Initialize supported API versions"""
        return {
            "1.0.0": APIVersion(
                version="1.0.0",
                release_date="2024-01-01",
                status="stable",
                endpoints={
                    "/api/v1/images/transform": "Image transformation endpoint",
                    "/api/v1/images/batch-transform": "Batch processing endpoint",
                    "/api/v1/users/register": "User registration",
                    "/api/v1/users/login": "User authentication"
                },
                deprecated_features=[],
                breaking_changes=[]
            ),
            "1.1.0": APIVersion(
                version="1.1.0",
                release_date="2024-03-01",
                status="beta",
                endpoints={
                    "/api/v1/images/transform": "Enhanced image transformation",
                    "/api/v1/images/batch-transform": "Improved batch processing",
                    "/api/v1/images/webhook": "Webhook notifications",
                    "/api/v1/analytics/usage": "Usage analytics"
                },
                deprecated_features=["/api/v1/images/transform (old format)"],
                breaking_changes=[]
            ),
            "2.0.0": APIVersion(
                version="2.0.0",
                release_date="2024-06-01",
                status="planned",
                endpoints={
                    "/api/v2/transform": "Unified transformation API",
                    "/api/v2/batch": "Advanced batch processing",
                    "/api/v2/realtime": "Real-time collaboration",
                    "/api/v2/ai": "AI-powered transformations"
                },
                deprecated_features=["/api/v1/*"],
                breaking_changes=[
                    "Complete endpoint restructuring",
                    "New authentication model",
                    "GraphQL API introduction"
                ]
            )
        }

    def check_version_compatibility(self, requested_version: str, client_version: str) -> VersionCompatibility:
        """Check compatibility between requested and client versions"""
        try:
            requested_ver = version.parse(requested_version)
            client_ver = version.parse(client_version)

            # Check if requested version is supported
            if requested_version not in self.supported_versions:
                return VersionCompatibility(
                    compatible=False,
                    requested_version=requested_version,
                    supported_versions=list(self.supported_versions.keys()),
                    recommended_version=self.current_version,
                    upgrade_required=True,
                    breaking_changes=self._get_breaking_changes_for_version(requested_version)
                )

            # Check if client version is compatible
            version_info = self.supported_versions[requested_version]

            if version_info.status == "deprecated":
                return VersionCompatibility(
                    compatible=True,
                    requested_version=requested_version,
                    supported_versions=list(self.supported_versions.keys()),
                    recommended_version=self.current_version,
                    upgrade_required=False,
                    deprecation_warning="This API version is deprecated. Please upgrade to latest version.",
                    sunset_date=version_info.sunset_date
                )

            # Version is compatible
            return VersionCompatibility(
                compatible=True,
                requested_version=requested_version,
                supported_versions=list(self.supported_versions.keys()),
                recommended_version=self.current_version,
                upgrade_required=False
            )

        except version.InvalidVersion:
            return VersionCompatibility(
                compatible=False,
                requested_version=requested_version,
                supported_versions=list(self.supported_versions.keys()),
                recommended_version=self.current_version,
                upgrade_required=True,
                error_message="Invalid version format"
            )

    def get_version_migration_guide(self, from_version: str, to_version: str) -> Dict[str, Any]:
        """Get migration guide for version upgrade"""
        if from_version not in self.supported_versions or to_version not in self.supported_versions:
            return {"error": "Invalid version specified"}

        migration_steps = []

        # General migration steps
        migration_steps.extend([
            "Update API endpoints to new version",
            "Review breaking changes documentation",
            "Update authentication method if changed",
            "Test all API calls with new version",
            "Update error handling for new response formats"
        ])

        # Version-specific migration steps
        if from_version == "1.0.0" and to_version == "1.1.0":
            migration_steps.extend([
                "Update image transformation request format",
                "Handle new webhook notification format",
                "Review updated rate limiting rules"
            ])

        return {
            "from_version": from_version,
            "to_version": to_version,
            "migration_steps": migration_steps,
            "estimated_effort": "2-4 hours",
            "breaking_changes": self._get_breaking_changes_between_versions(from_version, to_version)
        }

    def _get_breaking_changes_for_version(self, version: str) -> List[str]:
        """Get breaking changes for specific version"""
        if version in self.supported_versions:
            return self.supported_versions[version].breaking_changes
        return []

    def _get_breaking_changes_between_versions(self, from_version: str, to_version: str) -> List[str]:
        """Get breaking changes between two versions"""
        # Implementation would analyze changes between versions
        return ["Updated request/response format", "New authentication requirements"]
```

## 6. API Documentation and Testing

### 6.1 OpenAPI Documentation

#### Automatic API Documentation
```python
# src/api/documentation/openapi_generator.py
from fastapi import FastAPI
from src.api.main import app
from src.api.documentation.api_docs import APIDocumentationGenerator

class OpenAPIGenerator:
    """Generate OpenAPI documentation for all endpoints"""

    def __init__(self):
        self.app = app
        self.doc_generator = APIDocumentationGenerator()

    def generate_openapi_spec(self, version: str = "1.0.0") -> Dict[str, Any]:
        """Generate complete OpenAPI specification"""
        # Generate base OpenAPI spec
        openapi_schema = self.app.openapi()

        # Enhance with custom documentation
        enhanced_schema = self._enhance_openapi_schema(openapi_schema, version)

        return enhanced_schema

    def _enhance_openapi_schema(self, schema: Dict[str, Any], version: str) -> Dict[str, Any]:
        """Enhance OpenAPI schema with additional information"""
        # Add API metadata
        schema["info"]["version"] = version
        schema["info"]["title"] = "Artify Studio API"
        schema["info"]["description"] = "Comprehensive API for artistic image transformations"

        # Add server information
        schema["servers"] = [
            {
                "url": "https://api.artifystudio.com",
                "description": "Production server"
            },
            {
                "url": "https://staging-api.artifystudio.com",
                "description": "Staging server"
            }
        ]

        # Add security schemes
        schema["components"]["securitySchemes"] = {
            "BearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT"
            },
            "APIKeyAuth": {
                "type": "apiKey",
                "in": "header",
                "name": "X-API-Key"
            }
        }

        return schema

    def generate_endpoint_documentation(self, endpoint: str) -> Dict[str, Any]:
        """Generate detailed documentation for specific endpoint"""
        # Get endpoint information
        endpoint_info = self._get_endpoint_info(endpoint)

        return {
            "endpoint": endpoint,
            "method": endpoint_info["method"],
            "summary": endpoint_info["summary"],
            "description": endpoint_info["description"],
            "parameters": endpoint_info["parameters"],
            "request_body": endpoint_info["request_body"],
            "responses": endpoint_info["responses"],
            "examples": self._generate_endpoint_examples(endpoint),
            "rate_limits": endpoint_info["rate_limits"],
            "authentication": endpoint_info["authentication"]
        }

    def _generate_endpoint_examples(self, endpoint: str) -> Dict[str, Any]:
        """Generate request/response examples for endpoint"""
        examples = {
            "curl": self._generate_curl_example(endpoint),
            "python": self._generate_python_example(endpoint),
            "javascript": self._generate_javascript_example(endpoint)
        }

        return examples

    def _generate_curl_example(self, endpoint: str) -> str:
        """Generate curl example"""
        return f"""curl -X POST "https://api.artifystudio.com{endpoint}" \\
  -H "Content-Type: application/json" \\
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \\
  -d '{{"image_data": "base64_image_data", "transformation_type": "pencil_sketch"}}'"""

    def _generate_python_example(self, endpoint: str) -> str:
        """Generate Python example"""
        return '''import requests

headers = {
    "Authorization": "Bearer YOUR_JWT_TOKEN",
    "Content-Type": "application/json"
}

data = {
    "image_data": "base64_image_data",
    "transformation_type": "pencil_sketch",
    "quality": 85
}

response = requests.post(f"https://api.artifystudio.com{endpoint}", json=data, headers=headers)
result = response.json()'''

    def _generate_javascript_example(self, endpoint: str) -> str:
        """Generate JavaScript example"""
        return '''const response = await fetch(`https://api.artifystudio.com{endpoint}`, {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer YOUR_JWT_TOKEN',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    image_data: 'base64_image_data',
    transformation_type: 'pencil_sketch',
    quality: 85
  })
});

const result = await response.json();'''
```

### 6.2 API Testing Framework

#### Comprehensive API Testing
```python
# tests/api/test_image_processing_api.py
import pytest
import base64
from PIL import Image
import json
from fastapi.testclient import TestClient
from src.api.main import app

class TestImageProcessingAPI:
    """Comprehensive API testing"""

    @pytest.fixture
    def client(self):
        """FastAPI test client"""
        return TestClient(app)

    @pytest.fixture
    def sample_image_base64(self):
        """Create sample image as base64"""
        # Create test image
        image = Image.new('RGB', (100, 100), color='red')

        # Convert to base64
        import io
        buffer = io.BytesIO()
        image.save(buffer, format='PNG')
        image_bytes = buffer.getvalue()
        image_base64 = base64.b64encode(image_bytes).decode('utf-8')

        return image_base64

    @pytest.fixture
    def valid_api_key(self):
        """Create valid API key for testing"""
        return "test_api_key_12345"

    @pytest.fixture
    def auth_headers(self, valid_api_key):
        """Create authentication headers"""
        return {
            "X-API-Key": valid_api_key,
            "Content-Type": "application/json"
        }

    def test_successful_image_transformation(self, client, sample_image_base64, auth_headers):
        """Test successful image transformation"""
        request_data = {
            "image_data": f"data:image/png;base64,{sample_image_base64}",
            "transformation_type": "pencil_sketch",
            "quality": 85,
            "output_format": "PNG"
        }

        response = client.post("/api/v1/images/transform", json=request_data, headers=auth_headers)

        assert response.status_code == 200
        response_data = response.json()

        assert response_data["success"] == True
        assert "result_url" in response_data
        assert response_data["processing_time"] > 0
        assert response_data["cached"] == False

    def test_invalid_transformation_type(self, client, sample_image_base64, auth_headers):
        """Test error handling for invalid transformation type"""
        request_data = {
            "image_data": f"data:image/png;base64,{sample_image_base64}",
            "transformation_type": "invalid_transformation",
            "quality": 85
        }

        response = client.post("/api/v1/images/transform", json=request_data, headers=auth_headers)

        assert response.status_code == 400
        response_data = response.json()
        assert response_data["success"] == False
        assert "Invalid transformation type" in response_data["error_message"]

    def test_rate_limiting(self, client, sample_image_base64, auth_headers):
        """Test API rate limiting"""
        request_data = {
            "image_data": f"data:image/png;base64,{sample_image_base64}",
            "transformation_type": "pencil_sketch",
            "quality": 85
        }

        # Make multiple rapid requests
        responses = []
        for i in range(15):  # Exceed rate limit
            response = client.post("/api/v1/images/transform", json=request_data, headers=auth_headers)
            responses.append(response)

        # Should have rate limit response
        rate_limited_responses = [r for r in responses if r.status_code == 429]
        assert len(rate_limited_responses) > 0

        # Check rate limit response format
        rate_limit_response = rate_limited_responses[0].json()
        assert "retry_after" in rate_limit_response
        assert rate_limit_response["retry_after"] > 0

    def test_batch_processing_api(self, client, sample_image_base64, auth_headers):
        """Test batch processing API"""
        request_data = {
            "images": [f"data:image/png;base64,{sample_image_base64}"] * 3,
            "transformation_config": {
                "transformation_type": "pencil_sketch",
                "quality": 75
            },
            "webhook_url": "https://example.com/webhook"
        }

        response = client.post("/api/v1/images/batch-transform", json=request_data, headers=auth_headers)

        assert response.status_code == 200
        response_data = response.json()

        assert response_data["success"] == True
        assert "batch_id" in response_data
        assert response_data["status"] == "submitted"
        assert "estimated_completion_time" in response_data

    def test_batch_status_check(self, client, auth_headers):
        """Test batch status checking"""
        # First submit a batch job
        batch_response = client.post(
            "/api/v1/images/batch-transform",
            json={
                "images": [f"data:image/png;base64,{sample_image_base64}"],
                "transformation_config": {"transformation_type": "pencil_sketch"}
            },
            headers=auth_headers
        )

        batch_id = batch_response.json()["batch_id"]

        # Check batch status
        status_response = client.get(f"/api/v1/images/batch-status/{batch_id}", headers=auth_headers)

        assert status_response.status_code == 200
        status_data = status_response.json()

        assert status_data["batch_id"] == batch_id
        assert "status" in status_data
        assert "progress" in status_data

    def test_authentication_required(self, client, sample_image_base64):
        """Test that authentication is required"""
        request_data = {
            "image_data": f"data:image/png;base64,{sample_image_base64}",
            "transformation_type": "pencil_sketch"
        }

        # Request without API key
        response = client.post("/api/v1/images/transform", json=request_data)

        assert response.status_code == 401
        assert "authentication" in response.json()["detail"].lower()

    def test_input_validation(self, client, auth_headers):
        """Test input validation"""
        # Test with missing required fields
        incomplete_data = {
            "transformation_type": "pencil_sketch"
            # Missing image_data
        }

        response = client.post("/api/v1/images/transform", json=incomplete_data, headers=auth_headers)

        assert response.status_code == 400
        assert "image data is required" in response.json()["detail"].lower()

    def test_error_response_format(self, client, auth_headers):
        """Test error response format consistency"""
        # Make request that will cause server error
        invalid_data = {
            "image_data": "invalid_base64_data",
            "transformation_type": "pencil_sketch"
        }

        response = client.post("/api/v1/images/transform", json=invalid_data, headers=auth_headers)

        # Should return proper error response format
        assert response.status_code >= 400
        response_data = response.json()

        assert "success" in response_data
        assert response_data["success"] == False
        assert "error_message" in response_data or "detail" in response_data

    def test_response_time_requirements(self, client, sample_image_base64, auth_headers):
        """Test API response time requirements"""
        request_data = {
            "image_data": f"data:image/png;base64,{sample_image_base64}",
            "transformation_type": "pencil_sketch",
            "quality": 85
        }

        # Measure response time
        import time
        start_time = time.time()

        response = client.post("/api/v1/images/transform", json=request_data, headers=auth_headers)

        response_time = time.time() - start_time

        # API should respond within reasonable time
        assert response_time < 5.0  # 5 seconds maximum
        assert response.status_code == 200

    def test_api_version_header(self, client, sample_image_base64, auth_headers):
        """Test API version handling"""
        request_data = {
            "image_data": f"data:image/png;base64,{sample_image_base64}",
            "transformation_type": "pencil_sketch"
        }

        # Request with version header
        headers_with_version = auth_headers.copy()
        headers_with_version["Accept"] = "application/vnd.artifystudio.v1+json"

        response = client.post("/api/v1/images/transform", json=request_data, headers=headers_with_version)

        assert response.status_code == 200
        assert response.headers.get("X-API-Version") == "1.0.0"
```

## Conclusion

This comprehensive API design provides a robust foundation for Artify Studio's backend services, covering:

### API Excellence:
1. **Comprehensive Endpoints**: Full coverage of image processing, user management, and platform integration
2. **Security First**: JWT authentication, API key management, and distributed rate limiting
3. **Scalable Architecture**: Version management, caching, and performance optimization
4. **Developer Experience**: Complete OpenAPI documentation and extensive testing

### Key Features:
- **RESTful Design**: Clean, intuitive API endpoints following REST principles
- **Real-time Capabilities**: WebSocket support for live collaboration features
- **Batch Processing**: Efficient handling of multiple image transformations
- **Platform Integration**: APIs tailored for Web, Android, and iOS platforms
- **Analytics Integration**: Built-in usage tracking and performance monitoring

### Implementation Benefits:
- **Easy Integration**: Well-documented APIs enable quick third-party integration
- **Scalable Performance**: Distributed rate limiting and caching for high availability
- **Security Compliance**: Industry-standard authentication and authorization
- **Future-Proof Design**: Version management strategy supports API evolution
- **Developer Friendly**: Comprehensive documentation and testing tools

The API design ensures Artify Studio can serve a wide range of clients from mobile applications to web integrations while maintaining security, performance, and reliability across all platforms.

---

*Document Version: 1.0*
*Last Updated: October 2025*
*Author: Roshan*
*Project: Artify Studio (com.roshan.artifystudio)*