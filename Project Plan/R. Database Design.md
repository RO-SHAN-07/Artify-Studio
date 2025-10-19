# Artify Studio - Database Design

## 1. Database Architecture Overview

### 1.1 Data Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          Database Architecture                          │
├─────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │
│  │   User      │  │   Image     │  │   Processing│  │   Analytics │    │
│  │   Data      │  │   Data      │  │   Data      │  │   Data      │    │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘    │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │
│  │   Platform  │  │   Cache     │  │   Logs      │  │   Config    │    │
│  │   Data      │  │   Layer     │  │   Data      │  │   Data      │    │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘    │
├─────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │
│  │   SQLite    │  │   Redis     │  │   File      │  │   Cloud     │    │
│  │  (Mobile)   │  │   Cache     │  │   Storage   │  │   Storage   │    │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘    │
└─────────────────────────────────────────────────────────────────────────┘
```

### 1.2 Database Strategy by Platform

| Platform | Primary Database | Cache Layer | File Storage | Backup Strategy |
|----------|------------------|-------------|--------------|-----------------|
| **Web Platform** | PostgreSQL | Redis | AWS S3 | Automated daily |
| **Android** | SQLite | SharedPreferences | Internal/External | App backup integration |
| **iOS** | SQLite | NSCache | Document directory | iCloud backup |
| **Cross-Platform** | Platform abstraction | Redis/Memory | Unified API | Sync across platforms |

## 2. Core Database Schema

### 2.1 User Management Schema

#### Users Table
```sql
-- Core user information
CREATE TABLE users (
    user_id VARCHAR(36) PRIMARY KEY DEFAULT (uuid_generate_v4()),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    display_name VARCHAR(100),
    avatar_url VARCHAR(500),
    email_verified BOOLEAN DEFAULT FALSE,
    phone_number VARCHAR(20),
    phone_verified BOOLEAN DEFAULT FALSE,

    -- Account status
    account_status VARCHAR(20) DEFAULT 'active' CHECK (account_status IN ('active', 'suspended', 'deactivated')),
    account_type VARCHAR(20) DEFAULT 'free' CHECK (account_type IN ('free', 'premium', 'enterprise')),

    -- Subscription information
    subscription_plan VARCHAR(50),
    subscription_status VARCHAR(20) DEFAULT 'none',
    subscription_start_date TIMESTAMP,
    subscription_end_date TIMESTAMP,

    -- Platform information
    primary_platform VARCHAR(20) DEFAULT 'web',
    last_login_platform VARCHAR(20),
    last_login_ip INET,
    last_login_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Profile data
    preferences JSONB DEFAULT '{}',
    profile_data JSONB DEFAULT '{}',

    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL,

    -- Constraints
    CONSTRAINT valid_email_format CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
);

-- User sessions for web platform
CREATE TABLE user_sessions (
    session_id VARCHAR(128) PRIMARY KEY,
    user_id VARCHAR(36) REFERENCES users(user_id) ON DELETE CASCADE,
    platform VARCHAR(20) NOT NULL,
    device_info JSONB DEFAULT '{}',
    ip_address INET,
    user_agent TEXT,

    -- Session management
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,
    last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,

    -- Security
    refresh_token_hash VARCHAR(255),
    session_data JSONB DEFAULT '{}'
);

-- API keys for programmatic access
CREATE TABLE api_keys (
    key_id VARCHAR(36) PRIMARY KEY DEFAULT (uuid_generate_v4()),
    user_id VARCHAR(36) REFERENCES users(user_id) ON DELETE CASCADE,
    key_name VARCHAR(255) NOT NULL,
    api_key_hash VARCHAR(255) UNIQUE NOT NULL,
    key_permissions JSONB DEFAULT '{}',

    -- Rate limiting
    rate_limit_per_minute INTEGER DEFAULT 60,
    rate_limit_per_hour INTEGER DEFAULT 1000,
    rate_limit_per_day INTEGER DEFAULT 10000,

    -- Usage tracking
    total_requests BIGINT DEFAULT 0,
    last_used_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);
```

#### User Preferences Schema
```sql
-- Detailed user preferences
CREATE TABLE user_preferences (
    preference_id VARCHAR(36) PRIMARY KEY DEFAULT (uuid_generate_v4()),
    user_id VARCHAR(36) REFERENCES users(user_id) ON DELETE CASCADE,

    -- Transformation preferences
    default_transformation VARCHAR(50) DEFAULT 'pencil_sketch',
    default_quality INTEGER DEFAULT 85 CHECK (default_quality BETWEEN 1 AND 100),
    default_output_format VARCHAR(10) DEFAULT 'PNG',

    -- UI preferences
    theme VARCHAR(20) DEFAULT 'system',
    language VARCHAR(10) DEFAULT 'en',
    timezone VARCHAR(50) DEFAULT 'UTC',
    date_format VARCHAR(20) DEFAULT 'YYYY-MM-DD',
    auto_save BOOLEAN DEFAULT TRUE,
    show_tooltips BOOLEAN DEFAULT TRUE,

    -- Platform-specific preferences
    web_preferences JSONB DEFAULT '{}',
    android_preferences JSONB DEFAULT '{}',
    ios_preferences JSONB DEFAULT '{}',

    -- Notification preferences
    email_notifications BOOLEAN DEFAULT TRUE,
    push_notifications BOOLEAN DEFAULT TRUE,
    in_app_notifications BOOLEAN DEFAULT TRUE,
    notification_frequency VARCHAR(20) DEFAULT 'immediate',

    -- Privacy preferences
    analytics_opt_in BOOLEAN DEFAULT TRUE,
    crash_reporting_opt_in BOOLEAN DEFAULT TRUE,
    usage_data_collection BOOLEAN DEFAULT TRUE,

    -- Advanced preferences
    advanced_mode BOOLEAN DEFAULT FALSE,
    experimental_features BOOLEAN DEFAULT FALSE,
    performance_mode VARCHAR(20) DEFAULT 'balanced',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(user_id)
);
```

### 2.2 Image and Transformation Data Schema

#### Images Table
```sql
-- Image metadata and processing history
CREATE TABLE images (
    image_id VARCHAR(36) PRIMARY KEY DEFAULT (uuid_generate_v4()),
    user_id VARCHAR(36) REFERENCES users(user_id) ON DELETE CASCADE,

    -- File information
    original_filename VARCHAR(255) NOT NULL,
    file_size_bytes BIGINT NOT NULL,
    mime_type VARCHAR(100) NOT NULL,

    -- Image properties
    width INTEGER NOT NULL,
    height INTEGER NOT NULL,
    color_mode VARCHAR(20) NOT NULL, -- RGB, RGBA, Grayscale, etc.
    has_transparency BOOLEAN DEFAULT FALSE,
    aspect_ratio DECIMAL(5,3),

    -- Storage information
    storage_path VARCHAR(500) NOT NULL,
    thumbnail_path VARCHAR(500),
    storage_provider VARCHAR(50) DEFAULT 'local', -- local, s3, gcs, etc.

    -- Processing metadata
    processing_status VARCHAR(20) DEFAULT 'pending',
    processing_started_at TIMESTAMP,
    processing_completed_at TIMESTAMP,

    -- Content analysis
    content_tags JSONB DEFAULT '[]',
    dominant_colors JSONB DEFAULT '[]',
    image_complexity_score DECIMAL(3,2),

    -- Privacy and sharing
    is_public BOOLEAN DEFAULT FALSE,
    share_token VARCHAR(128) UNIQUE,
    download_count INTEGER DEFAULT 0,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL
);

-- Image transformations history
CREATE TABLE image_transformations (
    transformation_id VARCHAR(36) PRIMARY KEY DEFAULT (uuid_generate_v4()),
    image_id VARCHAR(36) REFERENCES images(image_id) ON DELETE CASCADE,
    user_id VARCHAR(36) REFERENCES users(user_id) ON DELETE CASCADE,

    -- Transformation details
    transformation_type VARCHAR(50) NOT NULL,
    transformation_parameters JSONB NOT NULL,
    quality INTEGER NOT NULL CHECK (quality BETWEEN 1 AND 100),
    output_format VARCHAR(10) NOT NULL,

    -- Processing information
    processing_time_ms INTEGER,
    processing_status VARCHAR(20) DEFAULT 'completed',
    error_message TEXT,

    -- Result information
    result_image_id VARCHAR(36) REFERENCES images(image_id),
    result_file_size_bytes BIGINT,
    result_path VARCHAR(500),

    -- Performance metrics
    cpu_usage_percent DECIMAL(5,2),
    memory_usage_mb INTEGER,
    gpu_utilization DECIMAL(5,2),

    -- Platform context
    processing_platform VARCHAR(20),
    device_info JSONB DEFAULT '{}',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processing_started_at TIMESTAMP,
    processing_completed_at TIMESTAMP
);
```

#### Batch Processing Schema
```sql
-- Batch processing jobs
CREATE TABLE batch_jobs (
    batch_id VARCHAR(36) PRIMARY KEY DEFAULT (uuid_generate_v4()),
    user_id VARCHAR(36) REFERENCES users(user_id) ON DELETE CASCADE,

    -- Job configuration
    job_name VARCHAR(255),
    transformation_config JSONB NOT NULL,
    total_images INTEGER NOT NULL,
    processed_images INTEGER DEFAULT 0,

    -- Job status
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'processing', 'completed', 'failed', 'cancelled')),
    progress_percent DECIMAL(5,2) DEFAULT 0,

    -- Timing
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    estimated_completion_at TIMESTAMP,

    -- Results
    successful_transformations INTEGER DEFAULT 0,
    failed_transformations INTEGER DEFAULT 0,
    results_summary JSONB DEFAULT '{}',

    -- Notifications
    webhook_url VARCHAR(500),
    webhook_attempts INTEGER DEFAULT 0,
    last_webhook_at TIMESTAMP,

    -- Error handling
    error_message TEXT,
    retry_count INTEGER DEFAULT 0,
    max_retries INTEGER DEFAULT 3
);

-- Individual batch items
CREATE TABLE batch_items (
    item_id VARCHAR(36) PRIMARY KEY DEFAULT (uuid_generate_v4()),
    batch_id VARCHAR(36) REFERENCES batch_jobs(batch_id) ON DELETE CASCADE,
    image_id VARCHAR(36) REFERENCES images(image_id) ON DELETE CASCADE,

    -- Item status
    status VARCHAR(20) DEFAULT 'pending',
    processing_order INTEGER NOT NULL,

    -- Processing details
    transformation_id VARCHAR(36) REFERENCES image_transformations(transformation_id),
    started_at TIMESTAMP,
    completed_at TIMESTAMP,

    -- Error handling
    error_message TEXT,
    retry_count INTEGER DEFAULT 0,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 2.3 Analytics and Usage Data Schema

#### Usage Analytics Schema
```sql
-- User activity tracking
CREATE TABLE user_activities (
    activity_id VARCHAR(36) PRIMARY KEY DEFAULT (uuid_generate_v4()),
    user_id VARCHAR(36) REFERENCES users(user_id) ON DELETE CASCADE,

    -- Activity details
    activity_type VARCHAR(50) NOT NULL, -- transformation, login, settings_change, etc.
    activity_category VARCHAR(50), -- image_processing, user_management, etc.
    platform VARCHAR(20) NOT NULL,
    session_id VARCHAR(128),

    -- Context information
    device_info JSONB DEFAULT '{}',
    browser_info JSONB DEFAULT '{}',
    location_info JSONB DEFAULT '{}',

    -- Activity data
    activity_data JSONB DEFAULT '{}',
    processing_time_ms INTEGER,
    image_count INTEGER DEFAULT 0,

    -- Performance metrics
    performance_score DECIMAL(3,2),
    error_occurred BOOLEAN DEFAULT FALSE,
    error_details JSONB,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Partition by date for performance
    PARTITION BY RANGE (created_at)
);

-- Daily usage summaries
CREATE TABLE daily_usage_summaries (
    summary_id VARCHAR(36) PRIMARY KEY DEFAULT (uuid_generate_v4()),
    user_id VARCHAR(36) REFERENCES users(user_id) ON DELETE CASCADE,
    summary_date DATE NOT NULL,

    -- Usage metrics
    total_sessions INTEGER DEFAULT 0,
    total_transformations INTEGER DEFAULT 0,
    total_images_processed INTEGER DEFAULT 0,
    total_processing_time_ms BIGINT DEFAULT 0,

    -- Platform breakdown
    web_usage_count INTEGER DEFAULT 0,
    android_usage_count INTEGER DEFAULT 0,
    ios_usage_count INTEGER DEFAULT 0,

    -- Feature usage
    transformations_used JSONB DEFAULT '{}',
    features_used JSONB DEFAULT '{}',

    -- Performance averages
    avg_processing_time_ms DECIMAL(10,2),
    avg_image_size_bytes INTEGER,
    success_rate DECIMAL(5,4),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(user_id, summary_date)
);

-- Platform performance metrics
CREATE TABLE platform_performance_metrics (
    metric_id VARCHAR(36) PRIMARY KEY DEFAULT (uuid_generate_v4()),
    platform VARCHAR(20) NOT NULL,
    metric_date DATE NOT NULL,

    -- Performance indicators
    avg_response_time_ms DECIMAL(10,2),
    avg_processing_time_ms DECIMAL(10,2),
    error_rate DECIMAL(5,4),
    uptime_percentage DECIMAL(5,2),

    -- Usage statistics
    total_requests INTEGER DEFAULT 0,
    unique_users INTEGER DEFAULT 0,
    total_transformations INTEGER DEFAULT 0,

    -- Resource utilization
    avg_cpu_usage DECIMAL(5,2),
    avg_memory_usage_mb INTEGER,
    avg_storage_usage_mb INTEGER,

    -- Platform-specific metrics
    platform_specific_data JSONB DEFAULT '{}',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(platform, metric_date)
);
```

### 2.4 Cache and Configuration Schema

#### Cache Management Schema
```sql
-- Cache entries for processed images
CREATE TABLE cache_entries (
    cache_key VARCHAR(255) PRIMARY KEY,
    cache_type VARCHAR(50) NOT NULL, -- image_result, transformation_preview, etc.

    -- Cache data
    data_path VARCHAR(500) NOT NULL,
    metadata JSONB DEFAULT '{}',

    -- Cache management
    size_bytes BIGINT NOT NULL,
    access_count INTEGER DEFAULT 0,
    last_accessed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Expiration
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,
    ttl_seconds INTEGER NOT NULL,

    -- Cache strategy
    cache_strategy VARCHAR(20) DEFAULT 'lru', -- lru, lfu, random
    priority INTEGER DEFAULT 1 -- 1-10, higher = more important
);

-- Cache statistics
CREATE TABLE cache_statistics (
    stat_id VARCHAR(36) PRIMARY KEY DEFAULT (uuid_generate_v4()),
    stat_date DATE NOT NULL,

    -- Hit/miss statistics
    total_requests INTEGER DEFAULT 0,
    cache_hits INTEGER DEFAULT 0,
    cache_misses INTEGER DEFAULT 0,
    hit_rate DECIMAL(5,4),

    -- Size and performance
    total_size_bytes BIGINT DEFAULT 0,
    entry_count INTEGER DEFAULT 0,
    avg_response_time_ms DECIMAL(10,2),

    -- Eviction statistics
    evictions_count INTEGER DEFAULT 0,
    evictions_by_size INTEGER DEFAULT 0,
    evictions_by_ttl INTEGER DEFAULT 0,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(stat_date)
);
```

#### Configuration Management Schema
```sql
-- System configuration
CREATE TABLE system_configurations (
    config_id VARCHAR(36) PRIMARY KEY DEFAULT (uuid_generate_v4()),
    config_key VARCHAR(255) UNIQUE NOT NULL,
    config_value JSONB NOT NULL,

    -- Configuration metadata
    config_type VARCHAR(50) NOT NULL, -- platform, feature, security, etc.
    platform VARCHAR(20),
    version VARCHAR(20),

    -- Configuration management
    is_active BOOLEAN DEFAULT TRUE,
    is_system_config BOOLEAN DEFAULT FALSE,
    requires_restart BOOLEAN DEFAULT FALSE,

    -- Audit trail
    created_by VARCHAR(36),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    change_reason TEXT
);

-- Feature flags and A/B testing
CREATE TABLE feature_flags (
    flag_id VARCHAR(36) PRIMARY KEY DEFAULT (uuid_generate_v4()),
    flag_key VARCHAR(255) UNIQUE NOT NULL,
    flag_name VARCHAR(255) NOT NULL,
    description TEXT,

    -- Flag configuration
    is_enabled BOOLEAN DEFAULT FALSE,
    rollout_percentage DECIMAL(5,2) DEFAULT 100.00,
    target_platforms JSONB DEFAULT '["web", "android", "ios"]',
    target_user_segments JSONB DEFAULT '[]',

    -- A/B testing
    is_ab_test BOOLEAN DEFAULT FALSE,
    test_groups JSONB DEFAULT '{}',

    -- Scheduling
    start_date TIMESTAMP,
    end_date TIMESTAMP,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 3. Platform-Specific Database Designs

### 3.1 Web Platform Database Schema

#### PostgreSQL Schema Extensions
```sql
-- Enable necessary extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_stat_statements";

-- Web-specific user sessions with detailed tracking
CREATE TABLE web_user_sessions (
    session_id VARCHAR(128) PRIMARY KEY,
    user_id VARCHAR(36) REFERENCES users(user_id) ON DELETE CASCADE,

    -- Browser and device information
    browser_name VARCHAR(50),
    browser_version VARCHAR(20),
    operating_system VARCHAR(50),
    device_type VARCHAR(50), -- desktop, tablet, mobile
    screen_resolution VARCHAR(20),

    -- Session tracking
    entry_page VARCHAR(500),
    exit_page VARCHAR(500),
    page_views INTEGER DEFAULT 0,
    session_duration_seconds INTEGER DEFAULT 0,

    -- Geographic information
    country_code VARCHAR(2),
    region VARCHAR(100),
    city VARCHAR(100),
    timezone VARCHAR(50),

    -- Technical details
    connection_type VARCHAR(50), -- wifi, cellular, ethernet
    bandwidth_estimate INTEGER, -- estimated bandwidth in Mbps

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ended_at TIMESTAMP NULL
);

-- Web analytics events
CREATE TABLE web_analytics_events (
    event_id VARCHAR(36) PRIMARY KEY DEFAULT (uuid_generate_v4()),
    session_id VARCHAR(128) REFERENCES web_user_sessions(session_id),
    user_id VARCHAR(36) REFERENCES users(user_id),

    -- Event details
    event_type VARCHAR(50) NOT NULL, -- page_view, button_click, transformation_start, etc.
    event_category VARCHAR(50),
    event_action VARCHAR(100),
    event_label VARCHAR(255),

    -- Event context
    page_url VARCHAR(500),
    referrer_url VARCHAR(500),
    element_selector VARCHAR(255),

    -- Event data
    event_data JSONB DEFAULT '{}',
    processing_time_ms INTEGER,

    -- Performance metrics
    dom_ready_time_ms INTEGER,
    load_time_ms INTEGER,
    first_paint_time_ms INTEGER,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 3.2 Mobile Platform Database Schema

#### Android SQLite Schema
```sql
-- Android-specific user data with offline support
CREATE TABLE android_user_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    sync_status TEXT DEFAULT 'synced', -- synced, pending, conflict

    -- Offline queue for sync
    pending_operations TEXT, -- JSON array of pending operations
    last_sync_timestamp INTEGER,
    sync_error TEXT,

    -- Device-specific data
    device_id TEXT NOT NULL,
    android_version TEXT,
    app_version TEXT,

    -- Local storage paths
    local_image_path TEXT,
    local_cache_path TEXT,

    created_at INTEGER DEFAULT (strftime('%s', 'now')),
    updated_at INTEGER DEFAULT (strftime('%s', 'now')),

    UNIQUE(user_id, device_id)
);

-- Android app settings
CREATE TABLE android_app_settings (
    setting_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT,

    -- Performance settings
    max_cache_size_mb INTEGER DEFAULT 100,
    enable_background_processing BOOLEAN DEFAULT TRUE,
    battery_optimization_mode TEXT DEFAULT 'balanced',

    -- Storage settings
    default_save_location TEXT DEFAULT 'internal',
    auto_backup_enabled BOOLEAN DEFAULT TRUE,
    backup_frequency TEXT DEFAULT 'daily',

    -- Notification settings
    push_notifications_enabled BOOLEAN DEFAULT TRUE,
    in_app_notifications_enabled BOOLEAN DEFAULT TRUE,
    notification_sound_enabled BOOLEAN DEFAULT TRUE,

    -- Privacy settings
    analytics_enabled BOOLEAN DEFAULT TRUE,
    crash_reporting_enabled BOOLEAN DEFAULT TRUE,

    created_at INTEGER DEFAULT (strftime('%s', 'now')),
    updated_at INTEGER DEFAULT (strftime('%s', 'now'))
);
```

#### iOS Core Data Schema
```sql
-- iOS-specific user preferences with iCloud sync
CREATE TABLE ios_user_preferences (
    preference_id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    device_id TEXT NOT NULL,

    -- iOS-specific settings
    icloud_sync_enabled BOOLEAN DEFAULT TRUE,
    haptic_feedback_enabled BOOLEAN DEFAULT TRUE,
    dark_mode_preference TEXT DEFAULT 'system',

    -- Siri integration
    siri_shortcuts_enabled BOOLEAN DEFAULT TRUE,
    siri_shortcuts JSON, -- Array of configured Siri shortcuts

    -- Widget configuration
    home_screen_widgets JSON, -- Widget configurations
    lock_screen_widgets JSON,

    -- Health and fitness (if applicable)
    health_kit_integration BOOLEAN DEFAULT FALSE,
    mindfulness_reminders BOOLEAN DEFAULT FALSE,

    -- Accessibility
    larger_text_enabled BOOLEAN DEFAULT FALSE,
    reduce_motion_enabled BOOLEAN DEFAULT FALSE,
    voice_over_enabled BOOLEAN DEFAULT FALSE,

    created_at REAL DEFAULT (datetime('now')),
    updated_at REAL DEFAULT (datetime('now')),

    UNIQUE(user_id, device_id)
);
```

## 4. Data Management and Optimization

### 4.1 Indexing Strategy

#### Performance Indexes
```sql
-- User-related indexes
CREATE INDEX idx_users_email ON users(email) WHERE deleted_at IS NULL;
CREATE INDEX idx_users_account_status ON users(account_status) WHERE deleted_at IS NULL;
CREATE INDEX idx_users_last_login ON users(last_login_timestamp DESC) WHERE deleted_at IS NULL;

-- Image-related indexes
CREATE INDEX idx_images_user_id ON images(user_id) WHERE deleted_at IS NULL;
CREATE INDEX idx_images_processing_status ON images(processing_status) WHERE deleted_at IS NULL;
CREATE INDEX idx_images_created_at ON images(created_at DESC) WHERE deleted_at IS NULL;
CREATE INDEX idx_images_is_public ON images(is_public) WHERE deleted_at IS NULL;

-- Transformation indexes
CREATE INDEX idx_transformations_image_id ON image_transformations(image_id);
CREATE INDEX idx_transformations_user_id ON image_transformations(user_id);
CREATE INDEX idx_transformations_type ON image_transformations(transformation_type);
CREATE INDEX idx_transformations_created_at ON image_transformations(created_at DESC);

-- Analytics indexes
CREATE INDEX idx_user_activities_user_id ON user_activities(user_id);
CREATE INDEX idx_user_activities_type ON user_activities(activity_type);
CREATE INDEX idx_user_activities_created_at ON user_activities(created_at DESC);
CREATE INDEX idx_user_activities_platform ON user_activities(platform);

-- Cache indexes
CREATE INDEX idx_cache_entries_type ON cache_entries(cache_type);
CREATE INDEX idx_cache_entries_accessed ON cache_entries(last_accessed_at DESC);
CREATE INDEX idx_cache_entries_expires ON cache_entries(expires_at);

-- Composite indexes for common queries
CREATE INDEX idx_images_user_public ON images(user_id, is_public) WHERE deleted_at IS NULL;
CREATE INDEX idx_transformations_user_type ON image_transformations(user_id, transformation_type);
CREATE INDEX idx_user_activities_user_platform ON user_activities(user_id, platform, created_at DESC);
```

### 4.2 Partitioning Strategy

#### Time-Based Partitioning
```sql
-- Partition user activities by month
CREATE TABLE user_activities_partitioned (
    LIKE user_activities INCLUDING ALL
) PARTITION BY RANGE (created_at);

-- Create monthly partitions
CREATE TABLE user_activities_2024_01 PARTITION OF user_activities_partitioned
    FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');

CREATE TABLE user_activities_2024_02 PARTITION OF user_activities_partitioned
    FOR VALUES FROM ('2024-02-01') TO ('2024-03-01');

-- Add more partitions as needed
```

### 4.3 Data Retention and Cleanup

#### Automated Cleanup Procedures
```sql
-- Procedure to clean up old cache entries
CREATE OR REPLACE FUNCTION cleanup_expired_cache()
RETURNS INTEGER AS $$
DECLARE
    deleted_count INTEGER;
BEGIN
    DELETE FROM cache_entries WHERE expires_at < NOW();
    GET DIAGNOSTICS deleted_count = ROW_COUNT;

    RETURN deleted_count;
END;
$$ LANGUAGE plpgsql;

-- Procedure to clean up old temporary files
CREATE OR REPLACE FUNCTION cleanup_temp_files()
RETURNS INTEGER AS $$
DECLARE
    deleted_count INTEGER;
BEGIN
    -- Delete temporary files older than 24 hours
    DELETE FROM images
    WHERE created_at < NOW() - INTERVAL '24 hours'
    AND processing_status = 'failed'
    AND deleted_at IS NULL;

    GET DIAGNOSTICS deleted_count = ROW_COUNT;

    RETURN deleted_count;
END;
$$ LANGUAGE plpgsql;

-- Procedure to archive old analytics data
CREATE OR REPLACE FUNCTION archive_old_analytics()
RETURNS INTEGER AS $$
DECLARE
    archived_count INTEGER;
BEGIN
    -- Move analytics data older than 1 year to archive table
    INSERT INTO user_activities_archive
    SELECT * FROM user_activities
    WHERE created_at < NOW() - INTERVAL '1 year';

    GET DIAGNOSTICS archived_count = ROW_COUNT;

    DELETE FROM user_activities
    WHERE created_at < NOW() - INTERVAL '1 year';

    RETURN archived_count;
END;
$$ LANGUAGE plpgsql;
```

## 5. Data Security and Privacy

### 5.1 Encryption Strategy

#### Data Encryption Implementation
```sql
-- Encrypted user data fields
ALTER TABLE users ADD COLUMN encrypted_personal_data BYTEA;

-- Function to encrypt sensitive data
CREATE OR REPLACE FUNCTION encrypt_sensitive_data(data TEXT, user_key TEXT)
RETURNS BYTEA AS $$
BEGIN
    -- Implementation would use AES-256 encryption
    -- This is a placeholder for the encryption logic
    RETURN ENCODE(DIGEST(data || user_key, 'sha256'), 'hex'::BYTEA);
END;
$$ LANGUAGE plpgsql;

-- Function to decrypt sensitive data
CREATE OR REPLACE FUNCTION decrypt_sensitive_data(encrypted_data BYTEA, user_key TEXT)
RETURNS TEXT AS $$
BEGIN
    -- Implementation would use AES-256 decryption
    -- This is a placeholder for the decryption logic
    RETURN 'decrypted_data';
END;
$$ LANGUAGE plpgsql;
```

### 5.2 Privacy Compliance Schema

#### GDPR Compliance Tracking
```sql
-- Data processing consent
CREATE TABLE data_processing_consent (
    consent_id VARCHAR(36) PRIMARY KEY DEFAULT (uuid_generate_v4()),
    user_id VARCHAR(36) REFERENCES users(user_id) ON DELETE CASCADE,

    -- Consent details
    consent_type VARCHAR(50) NOT NULL, -- analytics, marketing, third_party
    consent_status VARCHAR(20) DEFAULT 'granted', -- granted, denied, withdrawn
    consent_version VARCHAR(20) NOT NULL,

    -- Consent timing
    granted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    withdrawn_at TIMESTAMP,
    expires_at TIMESTAMP,

    -- Consent context
    ip_address INET,
    user_agent TEXT,
    consent_method VARCHAR(50), -- web_form, mobile_app, api

    -- Legal basis
    legal_basis VARCHAR(100), -- consent, legitimate_interest, legal_obligation
    privacy_policy_version VARCHAR(20),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Data deletion requests (GDPR Right to Erasure)
CREATE TABLE data_deletion_requests (
    request_id VARCHAR(36) PRIMARY KEY DEFAULT (uuid_generate_v4()),
    user_id VARCHAR(36) REFERENCES users(user_id) ON DELETE CASCADE,

    -- Request details
    request_type VARCHAR(50) NOT NULL, -- full_deletion, selective_deletion
    requested_by VARCHAR(36) NOT NULL, -- user_id or admin_id
    reason TEXT,

    -- Processing status
    status VARCHAR(20) DEFAULT 'pending',
    processing_started_at TIMESTAMP,
    processing_completed_at TIMESTAMP,

    -- Data to be deleted
    deletion_scope JSONB DEFAULT '{}', -- which data categories to delete
    affected_records_count INTEGER DEFAULT 0,

    -- Verification
    verification_token VARCHAR(128),
    verified_at TIMESTAMP,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 6. Database Performance Optimization

### 6.1 Query Optimization

#### Optimized Query Examples
```sql
-- Optimized user activity query with proper indexing
EXPLAIN ANALYZE
SELECT
    ua.activity_type,
    COUNT(*) as activity_count,
    AVG(ua.processing_time_ms) as avg_processing_time
FROM user_activities ua
WHERE ua.user_id = $1
    AND ua.created_at >= $2
    AND ua.created_at <= $3
    AND ua.platform = $4
GROUP BY ua.activity_type
ORDER BY activity_count DESC;

-- Optimized image search with multiple filters
EXPLAIN ANALYZE
SELECT
    i.image_id,
    i.original_filename,
    i.width,
    i.height,
    i.created_at,
    COUNT(t.transformation_id) as transformation_count
FROM images i
LEFT JOIN image_transformations t ON i.image_id = t.image_id
WHERE i.user_id = $1
    AND i.deleted_at IS NULL
    AND ($2 IS NULL OR i.width >= $2)
    AND ($3 IS NULL OR i.height >= $3)
    AND ($4 IS NULL OR i.created_at >= $4)
    AND ($5 IS NULL OR i.created_at <= $5)
GROUP BY i.image_id, i.original_filename, i.width, i.height, i.created_at
ORDER BY i.created_at DESC
LIMIT $6 OFFSET $7;
```

### 6.2 Connection Pooling Configuration

#### Database Connection Management
```python
# src/database/connection_manager.py
import asyncio
from typing import Optional, Dict, Any
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from src.database.config import DatabaseConfig

class DatabaseConnectionManager:
    """Manages database connections and pooling"""

    def __init__(self, config: DatabaseConfig):
        self.config = config
        self._engines: Dict[str, async_engine] = {}
        self._session_makers: Dict[str, async_sessionmaker] = {}

    def create_engine(self, database_type: str = 'primary') -> None:
        """Create database engine with optimized pooling"""
        if database_type == 'primary':
            connection_string = self.config.primary_database_url
            pool_config = {
                'pool_size': 20,
                'max_overflow': 30,
                'pool_pre_ping': True,
                'pool_recycle': 3600,
                'pool_timeout': 30
            }
        elif database_type == 'analytics':
            connection_string = self.config.analytics_database_url
            pool_config = {
                'pool_size': 10,
                'max_overflow': 15,
                'pool_pre_ping': True,
                'pool_recycle': 1800,
                'pool_timeout': 20
            }
        else:
            raise ValueError(f"Unknown database type: {database_type}")

        engine = create_async_engine(
            connection_string,
            **pool_config,
            echo=self.config.debug_mode
        )

        self._engines[database_type] = engine
        self._session_makers[database_type] = async_sessionmaker(
            engine, class_=AsyncSession, expire_on_commit=False
        )

    async def get_session(self, database_type: str = 'primary') -> AsyncSession:
        """Get database session"""
        if database_type not in self._engines:
            self.create_engine(database_type)

        session_maker = self._session_makers[database_type]
        return session_maker()

    async def execute_read_query(self, query, parameters=None, database_type: str = 'primary'):
        """Execute read query with connection pooling"""
        async with self.get_session(database_type) as session:
            result = await session.execute(query, parameters or {})
            return result.fetchall()

    async def execute_write_query(self, query, parameters=None, database_type: str = 'primary'):
        """Execute write query with transaction management"""
        async with self.get_session(database_type) as session:
            try:
                result = await session.execute(query, parameters or {})
                await session.commit()
                return result.rowcount
            except Exception as e:
                await session.rollback()
                raise e

    async def health_check(self) -> Dict[str, Any]:
        """Database health check"""
        health_status = {}

        for db_type in ['primary', 'analytics']:
            if db_type in self._engines:
                try:
                    start_time = asyncio.get_event_loop().time()
                    async with self.get_session(db_type) as session:
                        await session.execute("SELECT 1")
                    response_time = asyncio.get_event_loop().time() - start_time

                    health_status[db_type] = {
                        'status': 'healthy',
                        'response_time_ms': round(response_time * 1000, 2),
                        'connections_available': True
                    }
                except Exception as e:
                    health_status[db_type] = {
                        'status': 'unhealthy',
                        'error': str(e),
                        'connections_available': False
                    }
            else:
                health_status[db_type] = {
                    'status': 'not_configured'
                }

        return health_status
```

## 7. Data Migration and Versioning

### 7.1 Database Migration Strategy

#### Migration Management
```python
# src/database/migrations/migration_manager.py
from typing import List, Dict, Any
import asyncio
from src.database.migrations.versions import get_migrations

class DatabaseMigrationManager:
    """Manages database schema migrations"""

    def __init__(self, connection_manager: DatabaseConnectionManager):
        self.connection_manager = connection_manager
        self.migration_table = "schema_migrations"

    async def initialize_migration_system(self):
        """Initialize migration tracking system"""
        await self._create_migration_table()

    async def _create_migration_table(self):
        """Create table to track applied migrations"""
        query = f"""
        CREATE TABLE IF NOT EXISTS {self.migration_table} (
            migration_id VARCHAR(255) PRIMARY KEY,
            migration_name VARCHAR(255) NOT NULL,
            applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            checksum VARCHAR(64),
            execution_time_ms INTEGER,
            success BOOLEAN DEFAULT TRUE,
            error_message TEXT
        );
        """

        await self.connection_manager.execute_write_query(query)

    async def get_applied_migrations(self) -> List[str]:
        """Get list of already applied migrations"""
        query = f"SELECT migration_id FROM {self.migration_table} ORDER BY applied_at"
        result = await self.connection_manager.execute_read_query(query)
        return [row[0] for row in result]

    async def apply_migrations(self, target_version: str = None) -> Dict[str, Any]:
        """Apply pending migrations"""
        migrations = get_migrations()
        applied_migrations = await self.get_applied_migrations()

        pending_migrations = [
            migration for migration in migrations
            if migration['id'] not in applied_migrations
            and (target_version is None or migration['version'] <= target_version)
        ]

        results = {
            'success': True,
            'applied_migrations': [],
            'failed_migrations': [],
            'total_applied': 0
        }

        for migration in pending_migrations:
            try:
                start_time = asyncio.get_event_loop().time()

                # Apply migration
                await self._apply_single_migration(migration)

                execution_time = asyncio.get_event_loop().time() - start_time

                # Record successful migration
                await self._record_migration_success(
                    migration['id'],
                    migration['name'],
                    execution_time * 1000
                )

                results['applied_migrations'].append(migration['id'])
                results['total_applied'] += 1

            except Exception as e:
                # Record failed migration
                await self._record_migration_failure(
                    migration['id'],
                    migration['name'],
                    str(e)
                )

                results['failed_migrations'].append({
                    'migration_id': migration['id'],
                    'error': str(e)
                })
                results['success'] = False

                # Stop applying migrations on first failure
                break

        return results

    async def _apply_single_migration(self, migration: Dict[str, Any]):
        """Apply a single migration"""
        # Execute migration SQL
        for statement in migration['up_sql']:
            await self.connection_manager.execute_write_query(statement)

    async def _record_migration_success(self, migration_id: str, name: str, execution_time_ms: float):
        """Record successful migration"""
        query = f"""
        INSERT INTO {self.migration_table} (migration_id, migration_name, execution_time_ms, success)
        VALUES ($1, $2, $3, $4)
        """

        await self.connection_manager.execute_write_query(
            query,
            (migration_id, name, execution_time_ms, True)
        )

    async def rollback_migration(self, migration_id: str) -> Dict[str, Any]:
        """Rollback specific migration"""
        try:
            migrations = get_migrations()
            migration = next((m for m in migrations if m['id'] == migration_id), None)

            if not migration:
                return {
                    'success': False,
                    'error': f'Migration {migration_id} not found'
                }

            # Execute rollback SQL
            for statement in migration['down_sql']:
                await self.connection_manager.execute_write_query(statement)

            # Remove migration record
            query = f"DELETE FROM {self.migration_table} WHERE migration_id = $1"
            await self.connection_manager.execute_write_query(query, (migration_id,))

            return {
                'success': True,
                'rolled_back_migration': migration_id
            }

        except Exception as e:
            return {
                'success': False,
                'error': f'Rollback failed: {str(e)}'
            }
```

## Conclusion

This comprehensive database design provides a robust foundation for Artify Studio's data management needs across all platforms. The design covers:

### Database Excellence:
1. **Scalable Architecture**: Platform-specific optimizations with cross-platform data consistency
2. **Performance Optimized**: Comprehensive indexing, partitioning, and query optimization
3. **Security First**: Encryption, privacy compliance, and access control
4. **Analytics Ready**: Built-in analytics tracking and performance monitoring

### Key Features:
- **Multi-Platform Support**: Optimized schemas for Web, Android, and iOS platforms
- **Comprehensive Tracking**: User activities, image processing, and system performance
- **Privacy Compliant**: GDPR compliance with consent management and data deletion
- **Cache Management**: Intelligent caching with multiple strategies and analytics
- **Migration Support**: Automated schema versioning and migration management

### Implementation Benefits:
- **Data Consistency**: Unified data model across all platforms
- **Performance**: Optimized queries and indexing for fast data access
- **Scalability**: Partitioning and connection pooling for growth
- **Compliance**: Built-in privacy and security features
- **Maintainability**: Clear schema organization and migration strategy

The database design ensures Artify Studio can efficiently store, retrieve, and analyze user data while maintaining privacy, security, and performance across all supported platforms.

---

*Document Version: 1.0*
*Last Updated: October 2025*
*Author: Roshan*
*Project: Artify Studio (com.roshan.artifystudio)*