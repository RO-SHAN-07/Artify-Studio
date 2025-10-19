# Artify Studio - Error Handling Protocols

## 1. Error Classification System and Severity Levels

### 1.1 Error Classification Framework

#### Error Categories and Hierarchy
```
┌─────────────────────────────────────────────────────────────────────────┐
│                        Error Classification System                       │
├─────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │
│  │   Critical  │  │    High     │  │   Medium    │  │     Low     │    │
│  │   Errors    │  │   Errors    │  │   Errors    │  │   Errors    │    │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘    │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │
│  │ Application │  │ Data &      │  │ User        │  │ Performance │    │
│  │   Crash     │  │ Processing  │  │ Interface   │  │   Issues    │    │
│  │   Errors    │  │   Errors    │  │   Errors    │  │             │    │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘    │
├─────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │
│  │ Image       │  │ File        │  │ Platform    │  │ Network     │    │
│  │ Processing  │  │ System      │  │ Specific    │  │   Errors    │    │
│  │   Errors    │  │   Errors    │  │   Errors    │  │             │    │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘    │
└─────────────────────────────────────────────────────────────────────────┘
```

### 1.2 Severity Level Definitions

#### Critical Errors (Severity Level 1)
**Definition**: Errors that cause complete application failure or data loss
**Response Time**: Immediate (< 30 seconds)
**User Impact**: Application becomes unusable

**Examples**:
- Unhandled exceptions causing application crashes
- Memory allocation failures leading to termination
- Critical file system errors preventing operation
- Platform-specific crashes on startup

#### High Errors (Severity Level 2)
**Definition**: Errors that significantly impact core functionality
**Response Time**: < 5 minutes
**User Impact**: Major features become unavailable

**Examples**:
- Transformation engine failures
- Image processing pipeline errors
- File I/O errors preventing save/load operations
- Platform-specific rendering failures

#### Medium Errors (Severity Level 3)
**Definition**: Errors that affect specific features or user experience
**Response Time**: < 30 minutes
**User Impact**: Some features degraded but application functional

**Examples**:
- Individual transformation algorithm failures
- Preview generation errors
- Export format conversion issues
- UI component rendering problems

#### Low Errors (Severity Level 4)
**Definition**: Minor issues that don't affect core functionality
**Response Time**: < 2 hours
**User Impact**: Minimal or no impact on user experience

**Examples**:
- Warning messages for deprecated features
- Performance optimization suggestions
- Non-critical validation warnings
- Informational error messages

### 1.3 Error Code System

#### Standardized Error Codes
```python
# src/core/utils/error_codes.py
class ErrorCodes:
    """Standardized error codes for Artify Studio"""

    # Critical Errors (1000-1999)
    CRITICAL_APP_CRASH = "CRITICAL_001"
    CRITICAL_MEMORY_ERROR = "CRITICAL_002"
    CRITICAL_FILESYSTEM_ERROR = "CRITICAL_003"
    CRITICAL_PLATFORM_ERROR = "CRITICAL_004"

    # High Errors (2000-2999)
    HIGH_TRANSFORMATION_FAILED = "HIGH_001"
    HIGH_IMAGE_PROCESSING_ERROR = "HIGH_002"
    HIGH_FILE_IO_ERROR = "HIGH_003"
    HIGH_PLATFORM_RENDER_ERROR = "HIGH_004"

    # Medium Errors (3000-3999)
    MEDIUM_TRANSFORMATION_PARTIAL = "MEDIUM_001"
    MEDIUM_PREVIEW_ERROR = "MEDIUM_002"
    MEDIUM_EXPORT_ERROR = "MEDIUM_003"
    MEDIUM_UI_COMPONENT_ERROR = "MEDIUM_004"

    # Low Errors (4000-4999)
    LOW_VALIDATION_WARNING = "LOW_001"
    LOW_PERFORMANCE_WARNING = "LOW_002"
    LOW_FEATURE_DEPRECATION = "LOW_003"
    LOW_INFORMATIONAL = "LOW_004"

    # Platform-Specific Errors (5000-5999)
    PLATFORM_WEB_STREAMLIT_ERROR = "PLATFORM_001"
    PLATFORM_ANDROID_KIVY_ERROR = "PLATFORM_002"
    PLATFORM_IOS_KIVY_ERROR = "PLATFORM_003"
    PLATFORM_CROSS_PLATFORM_ERROR = "PLATFORM_004"
```

## 2. Platform-Specific Error Handling Strategies

### 2.1 Web Platform Error Handling (Streamlit)

#### Streamlit-Specific Error Management
```python
# src/platforms/web/error_handlers.py
import streamlit as st
import traceback
import logging
from typing import Dict, Any, Optional, Callable
from src.core.utils.error_codes import ErrorCodes

class StreamlitErrorHandler:
    """Error handling for Streamlit web platform"""

    def __init__(self):
        self.logger = logging.getLogger("artify_studio.web")
        self.error_history = []

    def handle_error(self, error: Exception, context: Dict[str, Any] = None):
        """Handle errors in Streamlit context"""
        error_info = {
            "error_type": type(error).__name__,
            "error_message": str(error),
            "traceback": traceback.format_exc(),
            "context": context or {},
            "timestamp": st.session_state.get('current_time', None),
            "user_id": st.session_state.get('user_id', 'anonymous')
        }

        # Classify error severity
        severity = self._classify_error_severity(error)

        # Log error
        self._log_error(error_info, severity)

        # Display user-friendly message
        self._display_user_message(error, severity)

        # Store in history for debugging
        self.error_history.append(error_info)

    def _classify_error_severity(self, error: Exception) -> str:
        """Classify error severity for web platform"""
        error_message = str(error).lower()

        # Critical errors
        if any(critical in error_message for critical in [
            "memory error", "out of memory", "killed", "segmentation fault"
        ]):
            return "critical"

        # High errors
        if any(high in error_message for high in [
            "transformation failed", "processing error", "opencv error",
            "pil error", "image processing failed"
        ]):
            return "high"

        # Medium errors
        if any(medium in error_message for medium in [
            "preview failed", "export error", "format error",
            "file save error", "load error"
        ]):
            return "medium"

        # Default to low
        return "low"

    def _log_error(self, error_info: Dict[str, Any], severity: str):
        """Log error with appropriate level"""
        log_message = f"[{severity.upper()}] {error_info['error_type']}: {error_info['error_message']}"

        if severity == "critical":
            self.logger.critical(log_message, extra=error_info)
        elif severity == "high":
            self.logger.error(log_message, extra=error_info)
        elif severity == "medium":
            self.logger.warning(log_message, extra=error_info)
        else:
            self.logger.info(log_message, extra=error_info)

    def _display_user_message(self, error: Exception, severity: str):
        """Display user-friendly error message"""
        if severity == "critical":
            st.error("🚨 **Critical Error**: The application encountered a serious issue and needs to restart. Please refresh the page.")
            st.error("If this problem persists, please contact support with the error details.")

        elif severity == "high":
            st.error("⚠️ **Processing Error**: Unable to complete the requested transformation.")
            with st.expander("Error Details"):
                st.code(str(error))

            # Offer retry option
            if st.button("🔄 Retry Operation"):
                st.rerun()

        elif severity == "medium":
            st.warning("⚡ **Minor Issue**: Some features may not work as expected.")
            with st.expander("Details"):
                st.text(str(error))

        else:
            st.info("ℹ️ **Notice**: " + str(error))

    def handle_transformation_error(self, transformation_type: str, error: Exception):
        """Handle transformation-specific errors"""
        context = {
            "transformation_type": transformation_type,
            "screen": "conversion_screen",
            "user_action": "apply_transformation"
        }

        self.handle_error(error, context)

        # Offer fallback options
        st.error(f"❌ **{transformation_type} Failed**")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Try Different Settings"):
                st.info("Please adjust the transformation parameters and try again.")

        with col2:
            if st.button("🎯 Try Different Transformation"):
                st.info("Consider using a different transformation type for your image.")

    def handle_file_upload_error(self, error: Exception, filename: str):
        """Handle file upload errors"""
        context = {
            "filename": filename,
            "screen": "file_upload",
            "user_action": "upload_image"
        }

        self.handle_error(error, context)

        st.error(f"❌ **Upload Failed**: {filename}")

        # Provide specific guidance based on error type
        error_msg = str(error).lower()

        if "format" in error_msg:
            st.info("💡 **Supported formats**: PNG, JPEG, WebP, TIFF, BMP")
        elif "size" in error_msg:
            st.info("💡 **Size limit**: Maximum 50MB per image")
        elif "corrupted" in error_msg:
            st.info("💡 **File integrity**: The file appears to be corrupted. Try re-saving the image.")

    def handle_export_error(self, error: Exception, export_format: str):
        """Handle export/save errors"""
        context = {
            "export_format": export_format,
            "screen": "export_screen",
            "user_action": "export_image"
        }

        self.handle_error(error, context)

        st.error(f"❌ **Export Failed**: Unable to save in {export_format} format")

        # Offer alternative formats
        st.info("🔄 **Try alternative formats**:")
        alt_formats = ["PNG", "JPEG", "WebP"]

        for fmt in alt_formats:
            if fmt != export_format:
                if st.button(f"💾 Export as {fmt}", key=f"export_{fmt}"):
                    # Implementation would retry export with different format
                    pass
```

### 2.2 Android Platform Error Handling (Kivy)

#### Kivy-Specific Error Management
```python
# src/platforms/android/error_handlers.py
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock
import logging
import traceback
import os
from typing import Dict, Any, Optional

class KivyErrorHandler:
    """Error handling for Kivy Android platform"""

    def __init__(self):
        self.logger = logging.getLogger("artify_studio.android")
        self.error_queue = []
        self.max_queue_size = 100

    def handle_error(self, error: Exception, context: Dict[str, Any] = None):
        """Handle errors in Kivy context"""
        error_info = {
            "error_type": type(error).__name__,
            "error_message": str(error),
            "traceback": traceback.format_exc(),
            "context": context or {},
            "timestamp": self._get_current_timestamp(),
            "device_info": self._get_device_info(),
            "app_version": self._get_app_version()
        }

        # Classify error severity
        severity = self._classify_error_severity(error)

        # Log error
        self._log_error(error_info, severity)

        # Display appropriate UI
        self._display_error_ui(error, severity)

        # Queue for crash reporting
        self._queue_error(error_info)

    def _classify_error_severity(self, error: Exception) -> str:
        """Classify error severity for Android platform"""
        error_message = str(error).lower()

        # Critical errors
        if any(critical in error_message for critical in [
            "memory error", "out of memory", "native crash", "sigsegv"
        ]):
            return "critical"

        # High errors
        if any(high in error_message for high in [
            "transformation failed", "opencv error", "camera error",
            "storage permission denied", "gpu error"
        ]):
            return "high"

        # Medium errors
        if any(medium in error_message for medium in [
            "preview failed", "export error", "file not found",
            "network unavailable", "battery low"
        ]):
            return "medium"

        return "low"

    def _log_error(self, error_info: Dict[str, Any], severity: str):
        """Log error to Android logging system"""
        log_message = f"[{severity.upper()}] {error_info['error_type']}: {error_info['error_message']}"

        if severity == "critical":
            self.logger.critical(log_message, extra=error_info)
        elif severity == "high":
            self.logger.error(log_message, extra=error_info)
        elif severity == "medium":
            self.logger.warning(log_message, extra=error_info)
        else:
            self.logger.info(log_message, extra=error_info)

        # Also log to Android logcat
        os.system(f"log -p {severity[0]} -t ArtifyStudio {log_message}")

    def _display_error_ui(self, error: Exception, severity: str):
        """Display error UI appropriate for mobile"""
        # Schedule on main thread
        Clock.schedule_once(lambda dt: self._show_error_popup(error, severity))

    def _show_error_popup(self, error: Exception, severity: str):
        """Show error popup with appropriate styling"""
        # Create popup content
        content = BoxLayout(orientation='vertical', spacing=10, padding=20)

        # Error icon and title based on severity
        if severity == "critical":
            title = "🚨 Critical Error"
            icon = "⚠️"
            bg_color = (1, 0.2, 0.2, 1)  # Red background
        elif severity == "high":
            title = "⚠️ Error"
            icon = "⚠️"
            bg_color = (1, 0.6, 0.2, 1)  # Orange background
        elif severity == "medium":
            title = "⚡ Warning"
            icon = "⚠️"
            bg_color = (1, 1, 0.2, 1)  # Yellow background
        else:
            title = "ℹ️ Notice"
            icon = "ℹ️"
            bg_color = (0.2, 0.6, 1, 1)  # Blue background

        # Title label
        title_label = Label(
            text=f"{icon} {title}",
            font_size=20,
            bold=True,
            size_hint_y=0.2
        )

        # Error message
        message_label = Label(
            text=str(error),
            font_size=16,
            size_hint_y=0.6,
            text_size=(300, None),
            halign='left',
            valign='top'
        )

        # Button layout
        button_layout = BoxLayout(orientation='horizontal', size_hint_y=0.2, spacing=10)

        if severity == "critical":
            # Restart button for critical errors
            restart_btn = Button(
                text="Restart App",
                background_color=(0.2, 0.8, 0.2, 1),
                on_press=self._restart_app
            )
            button_layout.add_widget(restart_btn)

        elif severity == "high":
            # Retry and dismiss buttons
            retry_btn = Button(
                text="Retry",
                background_color=(0.2, 0.8, 0.2, 1),
                on_press=self._retry_operation
            )
            dismiss_btn = Button(
                text="Dismiss",
                background_color=(0.6, 0.6, 0.6, 1),
                on_press=self._dismiss_error
            )
            button_layout.add_widget(retry_btn)
            button_layout.add_widget(dismiss_btn)

        else:
            # Single dismiss button
            dismiss_btn = Button(
                text="OK",
                background_color=(0.2, 0.6, 1, 1),
                on_press=self._dismiss_error
            )
            button_layout.add_widget(dismiss_btn)

        content.add_widget(title_label)
        content.add_widget(message_label)
        content.add_widget(button_layout)

        # Create and show popup
        popup = Popup(
            title="",
            content=content,
            size_hint=(0.9, 0.4),
            background_color=bg_color,
            auto_dismiss=False
        )

        popup.open()

    def _get_device_info(self) -> Dict[str, Any]:
        """Get Android device information"""
        try:
            return {
                "platform": "android",
                "android_version": self._get_android_version(),
                "device_model": self._get_device_model(),
                "available_memory": self._get_available_memory(),
                "battery_level": self._get_battery_level(),
                "storage_available": self._get_storage_available()
            }
        except Exception:
            return {"platform": "android"}

    def _get_android_version(self) -> str:
        """Get Android API version"""
        try:
            import android
            return str(android.get_android_version())
        except:
            return "unknown"

    def _get_device_model(self) -> str:
        """Get device model"""
        try:
            import android
            return android.get_device_model()
        except:
            return "unknown"

    def _get_available_memory(self) -> int:
        """Get available memory in MB"""
        try:
            import psutil
            return int(psutil.virtual_memory().available / 1024 / 1024)
        except:
            return 0

    def _get_battery_level(self) -> int:
        """Get battery level percentage"""
        try:
            import android
            return android.get_battery_level()
        except:
            return 100

    def _get_storage_available(self) -> int:
        """Get available storage in MB"""
        try:
            import android
            return int(android.get_storage_available() / 1024 / 1024)
        except:
            return 0

    def _get_current_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()

    def _get_app_version(self) -> str:
        """Get application version"""
        try:
            import android
            return android.get_package_version()
        except:
            return "1.0.0"

    def _restart_app(self, instance):
        """Restart the application"""
        App.get_running_app().stop()
        # On Android, the app will be restarted by the system

    def _retry_operation(self, instance):
        """Retry the failed operation"""
        # Implementation would retry the last operation
        popup = instance.parent.parent.parent  # Get popup reference
        popup.dismiss()

    def _dismiss_error(self, instance):
        """Dismiss the error popup"""
        popup = instance.parent.parent.parent  # Get popup reference
        popup.dismiss()

    def _queue_error(self, error_info: Dict[str, Any]):
        """Queue error for crash reporting"""
        self.error_queue.append(error_info)

        # Maintain queue size
        if len(self.error_queue) > self.max_queue_size:
            self.error_queue.pop(0)

    def flush_error_queue(self) -> List[Dict[str, Any]]:
        """Flush error queue for reporting"""
        errors = self.error_queue.copy()
        self.error_queue.clear()
        return errors

    def handle_memory_error(self, error: Exception):
        """Handle memory-specific errors"""
        context = {
            "error_type": "memory_error",
            "screen": "any",
            "user_action": "memory_intensive_operation"
        }

        self.handle_error(error, context)

        # Additional memory-specific handling
        self._trigger_garbage_collection()
        self._clear_caches()

    def _trigger_garbage_collection(self):
        """Trigger garbage collection"""
        import gc
        gc.collect()

    def _clear_caches(self):
        """Clear application caches"""
        # Implementation would clear image cache, transformation cache, etc.
        pass

    def handle_camera_error(self, error: Exception):
        """Handle camera-related errors"""
        context = {
            "error_type": "camera_error",
            "screen": "camera_screen",
            "user_action": "capture_image"
        }

        self.handle_error(error, context)

        # Provide camera-specific guidance
        self._show_camera_error_guidance(error)

    def _show_camera_error_guidance(self, error: Exception):
        """Show camera-specific error guidance"""
        error_msg = str(error).lower()

        if "permission" in error_msg:
            self._show_permission_guidance()
        elif "camera unavailable" in error_msg:
            self._show_camera_unavailable_guidance()
        elif "storage" in error_msg:
            self._show_storage_guidance()

    def _show_permission_guidance(self):
        """Show camera permission guidance"""
        content = BoxLayout(orientation='vertical', padding=20)

        content.add_widget(Label(
            text="📷 Camera Permission Required",
            font_size=18,
            bold=True
        ))

        content.add_widget(Label(
            text="To use the camera, please grant camera permission in Settings.",
            font_size=14,
            text_size=(280, None)
        ))

        # Settings button
        settings_btn = Button(
            text="Open Settings",
            background_color=(0.2, 0.6, 1, 1),
            on_press=self._open_app_settings
        )

        content.add_widget(settings_btn)

        popup = Popup(
            title="",
            content=content,
            size_hint=(0.8, 0.3)
        )

        popup.open()

    def _open_app_settings(self, instance):
        """Open application settings"""
        try:
            import android
            android.open_app_settings()
        except Exception as e:
            self.logger.error(f"Failed to open settings: {e}")

    def _show_camera_unavailable_guidance(self):
        """Show camera unavailable guidance"""
        content = BoxLayout(orientation='vertical', padding=20)

        content.add_widget(Label(
            text="📷 Camera Unavailable",
            font_size=18,
            bold=True
        ))

        content.add_widget(Label(
            text="Camera may be in use by another application or unavailable.",
            font_size=14,
            text_size=(280, None)
        ))

        content.add_widget(Button(
            text="Try Again",
            background_color=(0.2, 0.8, 0.2, 1),
            on_press=self._retry_camera
        ))

        popup = Popup(
            title="",
            content=content,
            size_hint=(0.8, 0.3)
        )

        popup.open()

    def _retry_camera(self, instance):
        """Retry camera operation"""
        popup = instance.parent.parent.parent
        popup.dismiss()
        # Implementation would retry camera initialization

    def _show_storage_guidance(self):
        """Show storage guidance"""
        content = BoxLayout(orientation='vertical', padding=20)

        content.add_widget(Label(
            text="💾 Storage Issue",
            font_size=18,
            bold=True
        ))

        content.add_widget(Label(
            text="Insufficient storage space or permission denied.",
            font_size=14,
            text_size=(280, None)
        ))

        content.add_widget(Button(
            text="Clear Cache",
            background_color=(1, 0.6, 0.2, 1),
            on_press=self._clear_app_cache
        ))

        popup = Popup(
            title="",
            content=content,
            size_hint=(0.8, 0.3)
        )

        popup.open()

    def _clear_app_cache(self, instance):
        """Clear application cache"""
        popup = instance.parent.parent.parent
        popup.dismiss()
        # Implementation would clear cache
```

### 2.3 iOS Platform Error Handling (Kivy)

#### iOS-Specific Error Management
```python
# src/platforms/ios/error_handlers.py
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
import logging
import traceback
import os
import platform
from typing import Dict, Any, Optional

class iOSErrorHandler:
    """Error handling for Kivy iOS platform"""

    def __init__(self):
        self.logger = logging.getLogger("artify_studio.ios")
        self.error_history = []

    def handle_error(self, error: Exception, context: Dict[str, Any] = None):
        """Handle errors in iOS context"""
        error_info = {
            "error_type": type(error).__name__,
            "error_message": str(error),
            "traceback": traceback.format_exc(),
            "context": context or {},
            "timestamp": self._get_current_timestamp(),
            "device_info": self._get_ios_device_info(),
            "ios_version": platform.mac_ver()[0] if platform.system() == "Darwin" else "unknown"
        }

        # Classify error severity
        severity = self._classify_ios_error_severity(error)

        # Log error
        self._log_ios_error(error_info, severity)

        # Display iOS-appropriate UI
        self._display_ios_error_ui(error, severity)

        # Store for crash reporting
        self.error_history.append(error_info)

    def _classify_ios_error_severity(self, error: Exception) -> str:
        """Classify error severity for iOS platform"""
        error_message = str(error).lower()

        # Critical errors
        if any(critical in error_message for critical in [
            "memory error", "out of memory", "killed", "exc_bad_access"
        ]):
            return "critical"

        # High errors
        if any(high in error_message for high in [
            "transformation failed", "opencv error", "camera error",
            "photo library access denied", "metal error"
        ]):
            return "high"

        # Medium errors
        if any(medium in error_message for medium in [
            "preview failed", "export error", "icloud sync error",
            "background task error", "low memory warning"
        ]):
            return "medium"

        return "low"

    def _log_ios_error(self, error_info: Dict[str, Any], severity: str):
        """Log error to iOS logging system"""
        log_message = f"[{severity.upper()}] {error_info['error_type']}: {error_info['error_message']}"

        if severity == "critical":
            self.logger.critical(log_message, extra=error_info)
        elif severity == "high":
            self.logger.error(log_message, extra=error_info)
        elif severity == "medium":
            self.logger.warning(log_message, extra=error_info)
        else:
            self.logger.info(log_message, extra=error_info)

        # Also log to iOS console
        print(f"ArtifyStudio: {log_message}")

    def _display_ios_error_ui(self, error: Exception, severity: str):
        """Display iOS-appropriate error UI"""
        # Use iOS haptic feedback for errors
        self._trigger_haptic_feedback(severity)

        # Show iOS-style alert
        self._show_ios_alert(error, severity)

    def _trigger_haptic_feedback(self, severity: str):
        """Trigger iOS haptic feedback"""
        try:
            if severity == "critical":
                # Heavy impact for critical errors
                import pyobjus
                # Implementation would use iOS haptic feedback APIs
                pass
            elif severity == "high":
                # Medium impact for high errors
                pass
            elif severity == "medium":
                # Light impact for medium errors
                pass
        except Exception:
            # Haptic feedback not available or failed
            pass

    def _show_ios_alert(self, error: Exception, severity: str):
        """Show iOS-style alert dialog"""
        # Create alert content
        content = BoxLayout(orientation='vertical', spacing=15, padding=20)

        # Title based on severity
        if severity == "critical":
            title_text = "Critical Error"
            title_color = (1, 0.2, 0.2, 1)
        elif severity == "high":
            title_text = "Error"
            title_color = (1, 0.6, 0.2, 1)
        elif severity == "medium":
            title_text = "Warning"
            title_color = (1, 1, 0.2, 1)
        else:
            title_text = "Notice"
            title_color = (0.2, 0.6, 1, 1)

        title_label = Label(
            text=title_text,
            font_size=20,
            bold=True,
            color=title_color,
            size_hint_y=0.2
        )

        # Error message
        message_label = Label(
            text=str(error),
            font_size=16,
            size_hint_y=0.5,
            text_size=(300, None),
            halign='left',
            valign='top'
        )

        # Button layout
        button_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=0.3,
            spacing=10
        )

        if severity == "critical":
            # Single OK button for critical errors
            ok_btn = Button(
                text="OK",
                background_color=(0.2, 0.6, 1, 1),
                on_press=self._dismiss_ios_alert
            )
            button_layout.add_widget(ok_btn)

        elif severity == "high":
            # Retry and OK buttons
            retry_btn = Button(
                text="Retry",
                background_color=(0.2, 0.8, 0.2, 1),
                on_press=self._retry_ios_operation
            )
            ok_btn = Button(
                text="OK",
                background_color=(0.6, 0.6, 0.6, 1),
                on_press=self._dismiss_ios_alert
            )
            button_layout.add_widget(retry_btn)
            button_layout.add_widget(ok_btn)

        else:
            # Single OK button
            ok_btn = Button(
                text="OK",
                background_color=(0.2, 0.6, 1, 1),
                on_press=self._dismiss_ios_alert
            )
            button_layout.add_widget(ok_btn)

        content.add_widget(title_label)
        content.add_widget(message_label)
        content.add_widget(button_layout)

        # Create iOS-style popup
        popup = Popup(
            title="",
            content=content,
            size_hint=(0.8, 0.4),
            background_color=(1, 1, 1, 0.95),
            auto_dismiss=False
        )

        popup.open()

    def _get_ios_device_info(self) -> Dict[str, Any]:
        """Get iOS device information"""
        try:
            return {
                "platform": "ios",
                "ios_version": platform.mac_ver()[0] if platform.system() == "Darwin" else "unknown",
                "device_model": self._get_ios_device_model(),
                "available_memory": self._get_ios_available_memory(),
                "battery_level": self._get_ios_battery_level(),
                "storage_available": self._get_ios_storage_available()
            }
        except Exception:
            return {"platform": "ios"}

    def _get_ios_device_model(self) -> str:
        """Get iOS device model"""
        try:
            import pyobjus
            # Implementation would use iOS APIs to get device model
            return "iPhone"  # Placeholder
        except:
            return "unknown"

    def _get_ios_available_memory(self) -> int:
        """Get available memory in MB"""
        try:
            import psutil
            return int(psutil.virtual_memory().available / 1024 / 1024)
        except:
            return 0

    def _get_ios_battery_level(self) -> int:
        """Get iOS battery level"""
        try:
            import pyobjus
            # Implementation would use iOS battery APIs
            return 100  # Placeholder
        except:
            return 100

    def _get_ios_storage_available(self) -> int:
        """Get available storage in MB"""
        try:
            import pyobjus
            # Implementation would use iOS storage APIs
            return 1000  # Placeholder
        except:
            return 0

    def _get_current_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()

    def _dismiss_ios_alert(self, instance):
        """Dismiss iOS alert"""
        popup = instance.parent.parent.parent
        popup.dismiss()

    def _retry_ios_operation(self, instance):
        """Retry iOS operation"""
        popup = instance.parent.parent.parent
        popup.dismiss()
        # Implementation would retry the failed operation

    def handle_photo_library_error(self, error: Exception):
        """Handle iOS Photo Library errors"""
        context = {
            "error_type": "photo_library_error",
            "screen": "photo_picker",
            "user_action": "access_photo_library"
        }

        self.handle_error(error, context)

        # Show iOS-specific photo library guidance
        self._show_photo_library_guidance(error)

    def _show_photo_library_guidance(self, error: Exception):
        """Show iOS Photo Library guidance"""
        error_msg = str(error).lower()

        if "permission" in error_msg:
            self._show_photo_permission_guidance()
        elif "icloud" in error_msg:
            self._show_icloud_guidance()
        elif "storage" in error_msg:
            self._show_storage_guidance()

    def _show_photo_permission_guidance(self):
        """Show iOS photo permission guidance"""
        content = BoxLayout(orientation='vertical', padding=20)

        content.add_widget(Label(
            text="📷 Photo Access Required",
            font_size=18,
            bold=True
        ))

        content.add_widget(Label(
            text="Please allow photo library access in Settings > Privacy > Photos.",
            font_size=14,
            text_size=(280, None)
        ))

        # Settings button
        settings_btn = Button(
            text="Open Settings",
            background_color=(0.2, 0.6, 1, 1),
            on_press=self._open_ios_settings
        )

        content.add_widget(settings_btn)

        popup = Popup(
            title="",
            content=content,
            size_hint=(0.8, 0.3)
        )

        popup.open()

    def _open_ios_settings(self, instance):
        """Open iOS settings"""
        try:
            import pyobjus
            # Implementation would use iOS APIs to open settings
            pass
        except Exception as e:
            self.logger.error(f"Failed to open iOS settings: {e}")

    def _show_icloud_guidance(self):
        """Show iCloud sync guidance"""
        content = BoxLayout(orientation='vertical', padding=20)

        content.add_widget(Label(
            text="☁️ iCloud Sync Issue",
            font_size=18,
            bold=True
        ))

        content.add_widget(Label(
            text="Please check your iCloud settings and internet connection.",
            font_size=14,
            text_size=(280, None)
        ))

        content.add_widget(Button(
            text="Check iCloud",
            background_color=(0.2, 0.6, 1, 1),
            on_press=self._check_icloud_settings
        ))

        popup = Popup(
            title="",
            content=content,
            size_hint=(0.8, 0.3)
        )

        popup.open()

    def _check_icloud_settings(self, instance):
        """Check iCloud settings"""
        popup = instance.parent.parent.parent
        popup.dismiss()
        # Implementation would check iCloud availability

    def _show_storage_guidance(self):
        """Show iOS storage guidance"""
        content = BoxLayout(orientation='vertical', padding=20)

        content.add_widget(Label(
            text="💾 Storage Full",
            font_size=18,
            bold=True
        ))

        content.add_widget(Label(
            text="Please free up storage space or enable iCloud Photos.",
            font_size=14,
            text_size=(280, None)
        ))

        content.add_widget(Button(
            text="Manage Storage",
            background_color=(1, 0.6, 0.2, 1),
            on_press=self._open_storage_settings
        ))

        popup = Popup(
            title="",
            content=content,
            size_hint=(0.8, 0.3)
        )

        popup.open()

    def _open_storage_settings(self, instance):
        """Open iOS storage settings"""
        try:
            import pyobjus
            # Implementation would use iOS APIs to open storage settings
            pass
        except Exception as e:
            self.logger.error(f"Failed to open storage settings: {e}")

    def handle_background_task_error(self, error: Exception):
        """Handle iOS background task errors"""
        context = {
            "error_type": "background_task_error",
            "screen": "background_processing",
            "user_action": "background_processing"
        }

        self.handle_error(error, context)

        # iOS-specific background task handling
        self._handle_background_task_limitation(error)

    def _handle_background_task_limitation(self, error: Exception):
        """Handle iOS background task limitations"""
        content = BoxLayout(orientation='vertical', padding=20)

        content.add_widget(Label(
            text="⏰ Background Processing Limited",
            font_size=18,
            bold=True
        ))

        content.add_widget(Label(
            text="iOS limits background processing. Please keep the app open for large transformations.",
            font_size=14,
            text_size=(280, None)
        ))

        content.add_widget(Button(
            text="Understood",
            background_color=(0.2, 0.6, 1, 1),
            on_press=self._dismiss_ios_alert
        ))

        popup = Popup(
            title="",
            content=content,
            size_hint=(0.8, 0.3)
        )

        popup.open()
```

## 3. Exception Handling Patterns for Image Processing Operations

### 3.1 Core Image Processing Error Handling

#### Image Loading and Validation Errors
```python
# src/core/io/error_handlers.py
import cv2
import numpy as np
from PIL import Image, UnidentifiedImageError
import os
from typing import Optional, Tuple, Dict, Any
from src.core.utils.error_codes import ErrorCodes

class ImageProcessingErrorHandler:
    """Error handling for image processing operations"""

    def __init__(self):
        self.logger = logging.getLogger("artify_studio.image_processing")

    def safe_image_load(self, file_path: str) -> Tuple[Optional[np.ndarray], Optional[str]]:
        """Safely load image with comprehensive error handling"""
        try:
            # Check file existence
            if not os.path.exists(file_path):
                return None, "File does not exist"

            # Check file size
            file_size = os.path.getsize(file_path)
            if file_size == 0:
                return None, "File is empty"

            if file_size > 50 * 1024 * 1024:  # 50MB limit
                return None, "File size exceeds 50MB limit"

            # Try PIL loading first
            try:
                with Image.open(file_path) as img:
                    # Validate image integrity
                    img.verify()

                    # Convert to RGB if necessary
                    if img.mode not in ('RGB', 'RGBA', 'L'):
                        img = img.convert('RGB')

                    # Convert to numpy array
                    image = np.array(img)

                    # Validate image array
                    if not self._validate_image_array(image):
                        return None, "Invalid image data"

                    return image, None

            except UnidentifiedImageError:
                return None, "Unsupported or corrupted image format"
            except Exception as e:
                return None, f"PIL error: {str(e)}"

        except PermissionError:
            return None, "Permission denied accessing file"
        except OSError as e:
            return None, f"File system error: {str(e)}"
        except Exception as e:
            self.logger.error(f"Unexpected error loading image {file_path}: {str(e)}")
            return None, f"Unexpected error: {str(e)}"

    def _validate_image_array(self, image: np.ndarray) -> bool:
        """Validate numpy image array"""
        try:
            # Check dimensions
            if len(image.shape) not in [2, 3]:
                return False

            # Check size constraints
            height, width = image.shape[:2]
            if height == 0 or width == 0:
                return False

            if height > 10000 or width > 10000:  # Reasonable upper limit
                return False

            # Check data type
            if image.dtype not in [np.uint8, np.float32, np.float64]:
                return False

            # Check for valid pixel values
            if image.dtype == np.uint8:
                if np.min(image) < 0 or np.max(image) > 255:
                    return False

            return True

        except Exception:
            return False

    def safe_opencv_operation(self, operation_func, *args, **kwargs) -> Tuple[Optional[Any], Optional[str]]:
        """Safely execute OpenCV operations"""
        try:
            result = operation_func(*args, **kwargs)
            return result, None

        except cv2.error as e:
            error_msg = str(e)
            if "OpenCV" in error_msg:
                return None, f"OpenCV processing error: {error_msg}"
            return None, f"Computer vision error: {error_msg}"

        except MemoryError:
            return None, "Insufficient memory for image processing operation"

        except Exception as e:
            return None, f"Unexpected error in image processing: {str(e)}"

    def safe_pillow_operation(self, operation_func, *args, **kwargs) -> Tuple[Optional[Any], Optional[str]]:
        """Safely execute Pillow operations"""
        try:
            result = operation_func(*args, **kwargs)
            return result, None

        except MemoryError:
            return None, "Insufficient memory for image operation"

        except OSError as e:
            return None, f"Image format error: {str(e)}"

        except Exception as e:
            return None, f"Pillow operation error: {str(e)}"

    def handle_transformation_error(self, transformation_type: str, error: Exception) -> Dict[str, Any]:
        """Handle transformation-specific errors"""
        error_info = {
            "error_code": ErrorCodes.HIGH_TRANSFORMATION_FAILED,
            "transformation_type": transformation_type,
            "error_message": str(error),
            "recoverable": self._is_transformation_error_recoverable(error),
            "fallback_options": self._get_transformation_fallbacks(transformation_type, error)
        }

        self.logger.error(f"Transformation error in {transformation_type}: {str(error)}")

        return error_info

    def _is_transformation_error_recoverable(self, error: Exception) -> bool:
        """Determine if transformation error is recoverable"""
        error_msg = str(error).lower()

        # Non-recoverable errors
        non_recoverable = [
            "memory error", "out of memory", "insufficient memory",
            "invalid image", "corrupted image", "unsupported format"
        ]

        return not any(term in error_msg for term in non_recoverable)

    def _get_transformation_fallbacks(self, transformation_type: str, error: Exception) -> list:
        """Get fallback options for failed transformations"""
        fallbacks = []

        if transformation_type == "pencil_sketch":
            fallbacks = [
                {"type": "colored_sketch", "reason": "Alternative sketch method"},
                {"type": "opencv_filters", "filter": "pencil_sketch_opencv", "reason": "OpenCV-based sketch"}
            ]

        elif transformation_type == "colored_sketch":
            fallbacks = [
                {"type": "pencil_sketch", "reason": "Grayscale version"},
                {"type": "opencv_filters", "filter": "stylization", "reason": "Color abstraction"}
            ]

        elif transformation_type == "turtle_graphics":
            fallbacks = [
                {"type": "pencil_sketch", "reason": "Edge-based alternative"},
                {"type": "opencv_filters", "filter": "edge_preserving", "reason": "Edge detection"}
            ]

        elif transformation_type == "opencv_filters":
            fallbacks = [
                {"type": "pencil_sketch", "reason": "CPU-based alternative"},
                {"type": "colored_sketch", "reason": "Different processing approach"}
            ]

        return fallbacks
```

### 3.2 Memory Management Error Handling

#### Memory Error Prevention and Recovery
```python
# src/core/utils/memory_handlers.py
import psutil
import gc
import os
import numpy as np
from typing import Dict, Any, Optional, Callable
import logging

class MemoryErrorHandler:
    """Memory error prevention and recovery"""

    def __init__(self):
        self.logger = logging.getLogger("artify_studio.memory")
        self.memory_limits = {
            "web": 512,      # MB
            "android": 256,  # MB
            "ios": 256       # MB
        }

    def check_memory_availability(self, required_mb: int = 50) -> Tuple[bool, str]:
        """Check if sufficient memory is available"""
        try:
            available_memory = psutil.virtual_memory().available / 1024 / 1024  # MB

            # Get platform-specific limit
            platform = self._detect_platform()
            memory_limit = self.memory_limits.get(platform, 256)

            if available_memory < required_mb:
                return False, f"Insufficient memory: {available_memory".1f"}MB available, {required_mb}MB required"

            if available_memory < memory_limit * 0.1:  # Less than 10% of limit
                return False, f"Low memory warning: {available_memory".1f"}MB available"

            return True, "Sufficient memory available"

        except Exception as e:
            return False, f"Memory check failed: {str(e)}"

    def safe_memory_allocation(self, shape: tuple, dtype: np.dtype, max_retries: int = 3) -> Optional[np.ndarray]:
        """Safely allocate memory with retry logic"""
        for attempt in range(max_retries):
            try:
                # Check memory before allocation
                required_mb = self._calculate_memory_requirement(shape, dtype)
                can_allocate, error_msg = self.check_memory_availability(required_mb)

                if not can_allocate:
                    if attempt == max_retries - 1:
                        self.logger.error(f"Memory allocation failed: {error_msg}")
                        return None

                    # Try garbage collection and retry
                    self._force_garbage_collection()
                    continue

                # Attempt allocation
                array = np.zeros(shape, dtype=dtype)

                # Verify allocation succeeded
                if array is not None:
                    return array

            except MemoryError as e:
                self.logger.warning(f"Memory allocation attempt {attempt + 1} failed: {str(e)}")

                if attempt == max_retries - 1:
                    self.logger.error("All memory allocation attempts failed")
                    return None

                # Try cleanup and retry
                self._cleanup_memory()
                continue

            except Exception as e:
                self.logger.error(f"Unexpected error during allocation: {str(e)}")
                return None

        return None

    def _calculate_memory_requirement(self, shape: tuple, dtype: np.dtype) -> int:
        """Calculate memory requirement for array"""
        try:
            # Calculate bytes per element
            bytes_per_element = np.dtype(dtype).itemsize

            # Calculate total elements
            total_elements = 1
            for dim in shape:
                total_elements *= dim

            # Calculate total bytes
            total_bytes = total_elements * bytes_per_element

            # Convert to MB
            total_mb = total_bytes / 1024 / 1024

            return int(total_mb)

        except Exception:
            # Default estimate
            return 50

    def _force_garbage_collection(self):
        """Force garbage collection"""
        try:
            gc.collect()
            gc.collect()  # Second collection for good measure

            # Also try to free unused memory
            if hasattr(gc, 'set_threshold'):
                gc.set_threshold(700, 10, 10)

        except Exception as e:
            self.logger.warning(f"Garbage collection failed: {str(e)}")

    def _cleanup_memory(self):
        """Clean up memory"""
        try:
            # Force garbage collection
            self._force_garbage_collection()

            # Clear any caches
            self._clear_caches()

            # Try to free system memory
            if os.name == 'posix':
                # On Unix systems, try to free page cache
                try:
                    os.system("sync")
                except:
                    pass

        except Exception as e:
            self.logger.warning(f"Memory cleanup failed: {str(e)}")

    def _clear_caches(self):
        """Clear application caches"""
        try:
            # Implementation would clear various caches
            # - Image cache
            # - Transformation cache
            # - Temporary file cache
            pass

        except Exception as e:
            self.logger.warning(f"Cache clearing failed: {str(e)}")

    def _detect_platform(self) -> str:
        """Detect current platform"""
        try:
            import platform
            system = platform.system().lower()

            if system == "darwin":
                return "ios" if "ios" in platform.platform().lower() else "ios"
            elif "android" in system or "linux" in system:
                # Check for Android
                if os.path.exists("/system/build.prop"):
                    return "android"
                return "web"  # Assume web for other Linux
            else:
                return "web"

        except Exception:
            return "web"

    def monitor_memory_usage(self, operation_name: str) -> Callable:
        """Decorator to monitor memory usage during operations"""
        def decorator(func):
            def wrapper(*args, **kwargs):
                try:
                    # Record initial memory
                    process = psutil.Process(os.getpid())
                    initial_memory = process.memory_info().rss / 1024 / 1024  # MB

                    # Execute function
                    result = func(*args, **kwargs)

                    # Record final memory
                    final_memory = process.memory_info().rss / 1024 / 1024  # MB
                    memory_used = final_memory - initial_memory

                    # Log memory usage
                    self.logger.info(f"{operation_name}: Memory usage = {memory_used".1f"}MB")

                    # Check for memory leaks
                    if memory_used > 100:  # More than 100MB used
                        self.logger.warning(f"High memory usage in {operation_name}: {memory_used".1f"}MB")

                    return result

                except Exception as e:
                    self.logger.error(f"Memory monitoring failed for {operation_name}: {str(e)}")
                    return func(*args, **kwargs)

            return wrapper
        return decorator
```

## 4. Logging and Monitoring Specifications

### 4.1 Centralized Logging System

#### Logging Configuration
```python
# src/core/utils/logging_config.py
import logging
import logging.handlers
import os
import sys
from pathlib import Path
from typing import Dict, Any

class LoggingConfig:
    """Centralized logging configuration"""

    def __init__(self, app_name: str = "artify_studio"):
        self.app_name = app_name
        self.log_directory = Path.home() / f".{app_name}" / "logs"
        self.log_directory.mkdir(parents=True, exist_ok=True)

    def setup_logging(self, platform: str = "web", debug: bool = False) -> None:
        """Setup logging configuration for platform"""
        # Clear existing handlers
        root_logger = logging.getLogger()
        root_logger.handlers.clear()

        # Set logging level
        log_level = logging.DEBUG if debug else logging.INFO

        # Create formatters
        detailed_formatter = logging.Formatter(
            fmt='%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        simple_formatter = logging.Formatter(
            fmt='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # Console handler (for development)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG if debug else logging.INFO)
        console_handler.setFormatter(detailed_formatter if debug else simple_formatter)

        # File handler
        log_file = self.log_directory / f"{self.app_name}_{platform}.log"
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        file_handler.setLevel(log_level)
        file_handler.setFormatter(detailed_formatter)

        # Platform-specific handlers
        if platform == "android":
            self._setup_android_logging(file_handler)
        elif platform == "ios":
            self._setup_ios_logging(file_handler)

        # Add handlers to root logger
        root_logger.addHandler(console_handler)
        root_logger.addHandler(file_handler)
        root_logger.setLevel(log_level)

        # Set specific levels for noisy libraries
        logging.getLogger("PIL").setLevel(logging.WARNING)
        logging.getLogger("matplotlib").setLevel(logging.WARNING)
        logging.getLogger("kivy").setLevel(logging.WARNING if not debug else logging.INFO)

    def _setup_android_logging(self, file_handler: logging.Handler) -> None:
        """Setup Android-specific logging"""
        try:
            # Also log to Android logcat
            logcat_handler = self._create_logcat_handler()
            if logcat_handler:
                logging.getLogger().addHandler(logcat_handler)

        except Exception as e:
            print(f"Failed to setup Android logging: {e}")

    def _setup_ios_logging(self, file_handler: logging.Handler) -> None:
        """Setup iOS-specific logging"""
        try:
            # iOS console logging is handled by the system
            pass

        except Exception as e:
            print(f"Failed to setup iOS logging: {e}")

    def _create_logcat_handler(self) -> Optional[logging.Handler]:
        """Create Android logcat handler"""
        try:
            class LogcatHandler(logging.Handler):
                def emit(self, record):
                    try:
                        log_entry = self.format(record)
                        os.system(f"log -p {record.levelno // 10} -t {self.app_name} {log_entry}")
                    except Exception:
                        pass

            return LogcatHandler()

        except Exception:
            return None

    def get_log_files(self) -> Dict[str, Path]:
        """Get paths to all log files"""
        return {
            "main": self.log_directory / f"{self.app_name}_web.log",
            "android": self.log_directory / f"{self.app_name}_android.log",
            "ios": self.log_directory / f"{self.app_name}_ios.log"
        }

    def cleanup_old_logs(self, days_to_keep: int = 7) -> None:
        """Clean up old log files"""
        try:
            import time

            cutoff_time = time.time() - (days_to_keep * 24 * 60 * 60)

            for log_file in self.log_directory.glob("*.log"):
                if log_file.stat().st_mtime < cutoff_time:
                    log_file.unlink()
                    self.logger.info(f"Cleaned up old log file: {log_file}")

        except Exception as e:
            self.logger.error(f"Failed to cleanup old logs: {e}")
```

### 4.2 Performance Monitoring Integration

#### Performance Metrics Collection
```python
# src/core/utils/performance_monitor.py
import time
import psutil
import os
import threading
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from collections import defaultdict, deque
import json

@dataclass
class PerformanceMetrics:
    """Performance metrics data structure"""
    timestamp: float
    operation_name: str
    duration_ms: float
    memory_used_mb: float
    cpu_percent: float
    success: bool
    error_message: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

class PerformanceMonitor:
    """Performance monitoring system"""

    def __init__(self, max_metrics: int = 1000):
        self.max_metrics = max_metrics
        self.metrics: deque = deque(maxlen=max_metrics)
        self.current_operations: Dict[str, float] = {}
        self.lock = threading.Lock()

    def start_operation(self, operation_name: str) -> str:
        """Start monitoring an operation"""
        operation_id = f"{operation_name}_{time.time()}_{threading.current_thread().ident}"

        with self.lock:
            self.current_operations[operation_id] = time.time()

        return operation_id

    def end_operation(self, operation_id: str, success: bool = True, error_message: str = None, **metadata) -> None:
        """End monitoring an operation"""
        with self.lock:
            if operation_id not in self.current_operations:
                return

            start_time = self.current_operations.pop(operation_id)
            duration = time.time() - start_time

            # Collect system metrics
            try:
                process = psutil.Process(os.getpid())
                memory_info = process.memory_info()
                cpu_percent = process.cpu_percent()

                metrics = PerformanceMetrics(
                    timestamp=time.time(),
                    operation_name=operation_id.split('_')[0],
                    duration_ms=duration * 1000,
                    memory_used_mb=memory_info.rss / 1024 / 1024,
                    cpu_percent=cpu_percent,
                    success=success,
                    error_message=error_message,
                    metadata=metadata
                )

                self.metrics.append(metrics)

            except Exception as e:
                # If system metrics fail, still record basic metrics
                metrics = PerformanceMetrics(
                    timestamp=time.time(),
                    operation_name=operation_id.split('_')[0],
                    duration_ms=duration * 1000,
                    memory_used_mb=0,
                    cpu_percent=0,
                    success=success,
                    error_message=error_message or f"Metrics collection failed: {str(e)}",
                    metadata=metadata
                )

                self.metrics.append(metrics)

    def get_metrics_summary(self, last_n: Optional[int] = None) -> Dict[str, Any]:
        """Get performance metrics summary"""
        with self.lock:
            metrics_to_analyze = list(self.metrics)[-last_n:] if last_n else list(self.metrics)

            if not metrics_to_analyze:
                return {"error": "No metrics available"}

            # Group by operation
            operation_stats = defaultdict(list)

            for metric in metrics_to_analyze:
                operation_stats[metric.operation_name].append(metric)

            # Calculate statistics
            summary = {}
            for operation, metrics in operation_stats.items():
                durations = [m.duration_ms for m in metrics if m.success]
                memory_usage = [m.memory_used_mb for m in metrics if m.success]
                success_rate = sum(1 for m in metrics if m.success) / len(metrics)

                summary[operation] = {
                    "count": len(metrics),
                    "success_rate": success_rate,
                    "avg_duration_ms": sum(durations) / len(durations) if durations else 0,
                    "max_duration_ms": max(durations) if durations else 0,
                    "avg_memory_mb": sum(memory_usage) / len(memory_usage) if memory_usage else 0,
                    "max_memory_mb": max(memory_usage) if memory_usage else 0,
                    "errors": [m.error_message for m in metrics if not m.success]
                }

            return {
                "total_operations": len(metrics_to_analyze),
                "time_range": {
                    "start": metrics_to_analyze[0].timestamp,
                    "end": metrics_to_analyze[-1].timestamp
                },
                "operation_stats": summary
            }

    def export_metrics(self, file_path: str) -> None:
        """Export metrics to JSON file"""
        with self.lock:
            metrics_data = [
                {
                    "timestamp": m.timestamp,
                    "operation_name": m.operation_name,
                    "duration_ms": m.duration_ms,
                    "memory_used_mb": m.memory_used_mb,
                    "cpu_percent": m.cpu_percent,
                    "success": m.success,
                    "error_message": m.error_message,
                    "metadata": m.metadata
                }
                for m in self.metrics
            ]

            try:
                with open(file_path, 'w') as f:
                    json.dump(metrics_data, f, indent=2)

            except Exception as e:
                print(f"Failed to export metrics: {e}")

    def clear_metrics(self) -> None:
        """Clear all stored metrics"""
        with self.lock:
            self.metrics.clear()
            self.current_operations.clear()
```

## 5. Error Recovery Workflows and Fallback Mechanisms

### 5.1 Transformation Error Recovery

#### Automatic Fallback System
```python
# src/core/engine/fallback_manager.py
from typing import Dict, Any, List, Optional, Callable
import logging
from src.core.utils.error_codes import ErrorCodes

class FallbackManager:
    """Manages fallback mechanisms for failed operations"""

    def __init__(self):
        self.logger = logging.getLogger("artify_studio.fallback")
        self.fallback_strategies = self._initialize_fallback_strategies()

    def _initialize_fallback_strategies(self) -> Dict[str, List[Dict[str, Any]]]:
        """Initialize fallback strategies for each transformation type"""
        return {
            "pencil_sketch": [
                {
                    "name": "reduce_quality",
                    "description": "Reduce processing quality to decrease memory usage",
                    "parameters": {"edge_intensity": 0.5, "shading_strength": 0.5},
                    "memory_reduction": 0.4
                },
                {
                    "name": "resize_image",
                    "description": "Resize image to smaller dimensions",
                    "parameters": {"max_dimension": 1024},
                    "memory_reduction": 0.6
                },
                {
                    "name": "opencv_fallback",
                    "description": "Use OpenCV-based pencil sketch",
                    "transformation_type": "opencv_filters",
                    "parameters": {"filter_type": "pencil_sketch_opencv"},
                    "memory_reduction": 0.3
                }
            ],
            "colored_sketch": [
                {
                    "name": "reduce_colors",
                    "description": "Reduce number of colors for processing",
                    "parameters": {"num_colors": 8},
                    "memory_reduction": 0.5
                },
                {
                    "name": "grayscale_fallback",
                    "description": "Fall back to grayscale pencil sketch",
                    "transformation_type": "pencil_sketch",
                    "parameters": {},
                    "memory_reduction": 0.7
                }
            ],
            "turtle_graphics": [
                {
                    "name": "simplify_contours",
                    "description": "Simplify contour detection for lower memory usage",
                    "parameters": {"contour_simplification": 0.05},
                    "memory_reduction": 0.4
                },
                {
                    "name": "edge_detection_fallback",
                    "description": "Use edge detection instead of full vectorization",
                    "transformation_type": "opencv_filters",
                    "parameters": {"filter_type": "edge_preserving"},
                    "memory_reduction": 0.6
                }
            ],
            "opencv_filters": [
                {
                    "name": "cpu_fallback",
                    "description": "Disable GPU acceleration and use CPU processing",
                    "parameters": {"enable_gpu_acceleration": False},
                    "memory_reduction": 0.2
                },
                {
                    "name": "simplified_algorithm",
                    "description": "Use simplified version of the algorithm",
                    "parameters": {"filter_strength": 0.3, "detail_preservation": 0.5},
                    "memory_reduction": 0.5
                }
            ]
        }

    def attempt_recovery(self, transformation_type: str, original_error: Exception,
                        original_parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Attempt to recover from transformation error"""
        self.logger.info(f"Attempting recovery for {transformation_type} after error: {str(original_error)}")

        # Get fallback strategies for this transformation
        strategies = self.fallback_strategies.get(transformation_type, [])

        if not strategies:
            return {
                "success": False,
                "error": "No fallback strategies available",
                "original_error": str(original_error)
            }

        # Try each strategy in order
        for strategy in strategies:
            try:
                recovery_result = self._try_fallback_strategy(
                    transformation_type, strategy, original_parameters, original_error
                )

                if recovery_result["success"]:
                    self.logger.info(f"Recovery successful using strategy: {strategy['name']}")
                    return recovery_result

            except Exception as e:
                self.logger.warning(f"Fallback strategy {strategy['name']} failed: {str(e)}")
                continue

        # All fallback strategies failed
        return {
            "success": False,
            "error": "All fallback strategies failed",
            "original_error": str(original_error),
            "attempted_strategies": [s["name"] for s in strategies]
        }

    def _try_fallback_strategy(self, transformation_type: str, strategy: Dict[str, Any],
                              original_parameters: Dict[str, Any], original_error: Exception) -> Dict[str, Any]:
        """Try a specific fallback strategy"""
        try:
            # Merge original parameters with fallback parameters
            fallback_parameters = original_parameters.copy()
            fallback_parameters.update(strategy.get("parameters", {}))

            # If strategy specifies a different transformation type, use that
            if "transformation_type" in strategy:
                actual_transformation_type = strategy["transformation_type"]
            else:
                actual_transformation_type = transformation_type

            # Here we would call the actual transformation engine
            # For now, simulate the result
            simulated_result = {
                "success": True,
                "transformation_type": actual_transformation_type,
                "parameters_used": fallback_parameters,
                "strategy_used": strategy["name"],
                "processing_time": 2.5,  # Simulated
                "memory_used": 100,      # Simulated MB
                "warning": f"Used fallback strategy: {strategy['description']}"
            }

            return simulated_result

        except Exception as e:
            return {
                "success": False,
                "error": f"Fallback strategy failed: {str(e)}",
                "strategy": strategy["name"]
            }
```

### 5.2 User-Friendly Error Recovery Interface

#### Error Recovery UI Components
```python
# src/core/ui/error_recovery.py
from typing import Dict, Any, List, Optional, Callable
import logging

class ErrorRecoveryInterface:
    """User interface for error recovery"""

    def __init__(self):
        self.logger = logging.getLogger("artify_studio.error_recovery")

    def show_recovery_options(self, error: Exception, transformation_type: str,
                            fallback_manager: FallbackManager) -> Dict[str, Any]:
        """Show recovery options to user"""
        # This would be implemented differently for each platform
        # Web: Streamlit components
        # Mobile: Native UI dialogs

        recovery_info = {
            "error_message": str(error),
            "transformation_type": transformation_type,
            "recovery_options": self._get_user_friendly_options(transformation_type, error),
            "can_retry": self._can_retry_operation(error),
            "can_use_alternative": self._can_use_alternative(error)
        }

        return recovery_info

    def _get_user_friendly_options(self, transformation_type: str, error: Exception) -> List[Dict[str, Any]]:
        """Get user-friendly recovery options"""
        options = []

        # Retry option
        if self._can_retry_operation(error):
            options.append({
                "type": "retry",
                "title": "🔄 Retry",
                "description": "Try the same operation again",
                "action": "retry_same"
            })

        # Alternative transformation options
        if self._can_use_alternative(error):
            alternatives = self._get_alternative_transformations(transformation_type)
            for alt in alternatives:
                options.append({
                    "type": "alternative",
                    "title": f"🎯 Try {alt['name']}",
                    "description": alt['description'],
                    "action": "use_alternative",
                    "alternative_type": alt['type']
                })

        # Adjust settings option
        if self._can_adjust_settings(error):
            options.append({
                "type": "adjust_settings",
                "title": "⚙️ Adjust Settings",
                "description": "Modify transformation parameters for better results",
                "action": "show_settings"
            })

        # Help option
        options.append({
            "type": "help",
            "title": "❓ Get Help",
            "description": "Learn more about this error and how to resolve it",
            "action": "show_help"
        })

        return options

    def _can_retry_operation(self, error: Exception) -> bool:
        """Determine if operation can be retried"""
        error_msg = str(error).lower()

        # Don't retry for these types of errors
        non_retryable = [
            "memory error", "out of memory", "insufficient memory",
            "invalid image", "corrupted image", "unsupported format",
            "permission denied", "file not found"
        ]

        return not any(term in error_msg for term in non_retryable)

    def _can_use_alternative(self, error: Exception) -> bool:
        """Determine if alternative transformation can be used"""
        error_msg = str(error).lower()

        # Can usually use alternative unless it's a fundamental issue
        fundamental_issues = [
            "memory error", "out of memory", "insufficient memory",
            "invalid image", "corrupted image"
        ]

        return not any(term in error_msg for term in fundamental_issues)

    def _can_adjust_settings(self, error: Exception) -> bool:
        """Determine if settings can be adjusted to resolve error"""
        error_msg = str(error).lower()

        # Can adjust settings for processing-related errors
        adjustable_errors = [
            "processing failed", "timeout", "quality too high",
            "parameter error", "convergence failed"
        ]

        return any(term in error_msg for term in adjustable_errors)

    def _get_alternative_transformations(self, transformation_type: str) -> List[Dict[str, Any]]:
        """Get alternative transformation options"""
        alternatives = {
            "pencil_sketch": [
                {"type": "colored_sketch", "name": "Colored Sketch", "description": "Create a colored version instead"},
                {"type": "opencv_filters", "name": "OpenCV Filters", "description": "Use OpenCV-based artistic filters"}
            ],
            "colored_sketch": [
                {"type": "pencil_sketch", "name": "Pencil Sketch", "description": "Create a grayscale version instead"},
                {"type": "opencv_filters", "name": "OpenCV Filters", "description": "Use OpenCV-based artistic filters"}
            ],
            "turtle_graphics": [
                {"type": "pencil_sketch", "name": "Pencil Sketch", "description": "Create a sketch-based version"},
                {"type": "opencv_filters", "name": "OpenCV Filters", "description": "Use edge-preserving filters"}
            ],
            "opencv_filters": [
                {"type": "pencil_sketch", "name": "Pencil Sketch", "description": "Use CPU-based sketch transformation"},
                {"type": "colored_sketch", "name": "Colored Sketch", "description": "Use color-based sketch transformation"}
            ]
        }

        return alternatives.get(transformation_type, [])

    def create_recovery_workflow(self, error: Exception, context: Dict[str, Any]) -> Dict[str, Any]:
        """Create a complete error recovery workflow"""
        workflow = {
            "error_id": f"error_{int(time.time())}_{id(error)}",
            "error_type": type(error).__name__,
            "error_message": str(error),
            "context": context,
            "steps": self._create_recovery_steps(error, context),
            "estimated_recovery_time": self._estimate_recovery_time(error),
            "success_probability": self._estimate_success_probability(error)
        }

        return workflow

    def _create_recovery_steps(self, error: Exception, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create step-by-step recovery instructions"""
        steps = []

        # Step 1: Immediate action
        if self._can_retry_operation(error):
            steps.append({
                "step": 1,
                "action": "retry",
                "description": "Try the operation again with the same settings",
                "estimated_time": "10 seconds",
                "success_rate": 0.8
            })

        # Step 2: Alternative approach
        if self._can_use_alternative(error):
            steps.append({
                "step": 2,
                "action": "alternative",
                "description": "Use a different transformation type",
                "estimated_time": "30 seconds",
                "success_rate": 0.9
            })

        # Step 3: Settings adjustment
        if self._can_adjust_settings(error):
            steps.append({
                "step": 3,
                "action": "adjust_settings",
                "description": "Modify transformation parameters",
                "estimated_time": "1 minute",
                "success_rate": 0.7
            })

        # Step 4: Technical support
        steps.append({
            "step": 4,
            "action": "contact_support",
            "description": "Contact support if issue persists",
            "estimated_time": "5 minutes",
            "success_rate": 0.95
        })

        return steps

    def _estimate_recovery_time(self, error: Exception) -> str:
        """Estimate total recovery time"""
        error_msg = str(error).lower()

        if "memory" in error_msg:
            return "2-5 minutes"
        elif "processing" in error_msg:
            return "30 seconds - 2 minutes"
        elif "file" in error_msg:
            return "1-3 minutes"
        else:
            return "1-5 minutes"

    def _estimate_success_probability(self, error: Exception) -> float:
        """Estimate probability of successful recovery"""
        error_msg = str(error).lower()

        if "memory" in error_msg:
            return 0.6  # Memory issues are often recoverable
        elif "processing" in error_msg:
            return 0.8  # Processing issues usually have alternatives
        elif "file" in error_msg:
            return 0.4  # File issues depend on the specific problem
        else:
            return 0.7  # Default moderate success rate
```

## 6. Platform-Specific Error Scenarios and Solutions

### 6.1 Web Platform Error Scenarios

#### Common Streamlit-Specific Errors
```python
# src/platforms/web/error_scenarios.py
class WebErrorScenarios:
    """Common error scenarios for web platform"""

    @staticmethod
    def handle_browser_memory_limit(file_size_mb: int) -> Dict[str, Any]:
        """Handle browser memory limit exceeded"""
        return {
            "error_code": ErrorCodes.CRITICAL_MEMORY_ERROR,
            "user_message": "Image too large for browser processing",
            "technical_message": f"File size {file_size_mb}MB exceeds browser memory limits",
            "solutions": [
                "Resize image to under 10MB",
                "Use a different browser",
                "Enable more RAM for browser tab",
                "Process image in smaller chunks"
            ],
            "fallback_available": True,
            "fallback_action": "resize_image"
        }

    @staticmethod
    def handle_session_timeout() -> Dict[str, Any]:
        """Handle Streamlit session timeout"""
        return {
            "error_code": ErrorCodes.HIGH_PLATFORM_RENDER_ERROR,
            "user_message": "Session expired",
            "technical_message": "Streamlit session timed out during processing",
            "solutions": [
                "Refresh the page and try again",
                "Process smaller images",
                "Check internet connection stability"
            ],
            "fallback_available": True,
            "fallback_action": "restart_session"
        }

    @staticmethod
    def handle_cors_error() -> Dict[str, Any]:
        """Handle Cross-Origin Resource Sharing errors"""
        return {
            "error_code": ErrorCodes.MEDIUM_PLATFORM_RENDER_ERROR,
            "user_message": "Unable to load external resources",
            "technical_message": "CORS policy blocking resource access",
            "solutions": [
                "Ensure all resources are served from same domain",
                "Configure proper CORS headers on server",
                "Use data URLs for images when possible"
            ],
            "fallback_available": False,
            "fallback_action": None
        }
```

### 6.2 Android Platform Error Scenarios

#### Common Kivy Android Errors
```python
# src/platforms/android/error_scenarios.py
class AndroidErrorScenarios:
    """Common error scenarios for Android platform"""

    @staticmethod
    def handle_storage_permission_denied() -> Dict[str, Any]:
        """Handle storage permission denied"""
        return {
            "error_code": ErrorCodes.HIGH_FILE_IO_ERROR,
            "user_message": "Storage access required",
            "technical_message": "Storage permission denied by user or system",
            "solutions": [
                "Grant storage permission in app settings",
                "Check if storage is available and not full",
                "Try restarting the app",
                "Check if device has sufficient space"
            ],
            "fallback_available": True,
            "fallback_action": "request_permission_again"
        }

    @staticmethod
    def handle_camera_unavailable() -> Dict[str, Any]:
        """Handle camera unavailable errors"""
        return {
            "error_code": ErrorCodes.HIGH_PLATFORM_RENDER_ERROR,
            "user_message": "Camera not available",
            "technical_message": "Camera hardware unavailable or in use",
            "solutions": [
                "Close other camera apps",
                "Restart the device",
                "Check camera permissions",
                "Use gallery instead of camera"
            ],
            "fallback_available": True,
            "fallback_action": "use_gallery"
        }

    @staticmethod
    def handle_battery_optimization() -> Dict[str, Any]:
        """Handle battery optimization restrictions"""
        return {
            "error_code": ErrorCodes.MEDIUM_PLATFORM_RENDER_ERROR,
            "user_message": "Background processing limited",
            "technical_message": "Battery optimization preventing background processing",
            "solutions": [
                "Disable battery optimization for Artify Studio",
                "Keep app in foreground during processing",
                "Process smaller images",
                "Schedule processing when device is charging"
            ],
            "fallback_available": True,
            "fallback_action": "reduce_processing_priority"
        }

    @staticmethod
    def handle_gpu_unavailable() -> Dict[str, Any]:
        """Handle GPU acceleration unavailable"""
        return {
            "error_code": ErrorCodes.MEDIUM_PLATFORM_RENDER_ERROR,
            "user_message": "GPU acceleration unavailable",
            "technical_message": "OpenCL/OpenGL ES not available on device",
            "solutions": [
                "Use CPU-based processing",
                "Update device drivers",
                "Check GPU compatibility",
                "Restart graphics system"
            ],
            "fallback_available": True,
            "fallback_action": "disable_gpu_acceleration"
        }
```

### 6.3 iOS Platform Error Scenarios

#### Common Kivy iOS Errors
```python
# src/platforms/ios/error_scenarios.py
class iOSErrorScenarios:
    """Common error scenarios for iOS platform"""

    @staticmethod
    def handle_photo_library_restricted() -> Dict[str, Any]:
        """Handle Photo Library access restrictions"""
        return {
            "error_code": ErrorCodes.HIGH_FILE_IO_ERROR,
            "user_message": "Photo Library access restricted",
            "technical_message": "Photo Library access denied or restricted",
            "solutions": [
                "Allow Photo Library access in Settings > Privacy > Photos",
                "Check Screen Time restrictions",
                "Ensure iCloud Photos is enabled",
                "Try restarting the device"
            ],
            "fallback_available": True,
            "fallback_action": "use_camera_instead"
        }

    @staticmethod
    def handle_icloud_sync_error() -> Dict[str, Any]:
        """Handle iCloud sync errors"""
        return {
            "error_code": ErrorCodes.MEDIUM_FILE_IO_ERROR,
            "user_message": "iCloud sync issue",
            "technical_message": "iCloud synchronization failed",
            "solutions": [
                "Check internet connection",
                "Verify iCloud storage availability",
                "Sign out and back into iCloud",
                "Check iCloud Photos settings"
            ],
            "fallback_available": True,
            "fallback_action": "use_local_storage"
        }

    @staticmethod
    def handle_background_app_refresh() -> Dict[str, Any]:
        """Handle background app refresh restrictions"""
        return {
            "error_code": ErrorCodes.MEDIUM_PLATFORM_RENDER_ERROR,
            "user_message": "Background processing disabled",
            "technical_message": "Background App Refresh disabled for Artify Studio",
            "solutions": [
                "Enable Background App Refresh in Settings",
                "Keep app in foreground during processing",
                "Process images when app is active",
                "Check Low Power Mode settings"
            ],
            "fallback_available": True,
            "fallback_action": "foreground_processing_only"
        }

    @staticmethod
    def handle_metal_unavailable() -> Dict[str, Any]:
        """Handle Metal framework unavailable"""
        return {
            "error_code": ErrorCodes.MEDIUM_PLATFORM_RENDER_ERROR,
            "user_message": "Graphics acceleration unavailable",
            "technical_message": "Metal framework not available on this device",
            "solutions": [
                "Use CPU-based processing",
                "Update to newer iOS version",
                "Check device compatibility",
                "Restart graphics services"
            ],
            "fallback_available": True,
            "fallback_action": "disable_metal_acceleration"
        }
```

## Conclusion

This comprehensive error handling protocol provides a robust framework for managing errors across all platforms in Artify Studio. The system includes:

1. **Structured Error Classification**: Four-tier severity system with specific response times
2. **Platform-Specific Handling**: Tailored error management for Web, Android, and iOS
3. **Comprehensive Recovery Mechanisms**: Automatic fallback strategies and user-guided recovery
4. **Advanced Monitoring**: Performance tracking and logging integration
5. **User-Friendly Interface**: Clear error messages with actionable solutions

**Key Benefits:**
- **Improved User Experience**: Users receive helpful guidance instead of cryptic errors
- **Higher Success Rate**: Automatic fallback mechanisms increase operation success
- **Better Debugging**: Comprehensive logging aids in issue resolution
- **Platform Consistency**: Unified error handling approach across all platforms
- **Proactive Monitoring**: Early detection of issues before they become critical

**Implementation Priority:**
1. Implement core error classification and logging
2. Add platform-specific error handlers
3. Integrate automatic fallback mechanisms
4. Develop user-friendly recovery interfaces
5. Set up comprehensive monitoring and alerting

---

*Document Version: 1.0*
*Last Updated: October 2025*
*Author: Roshan*
*Project: Artify Studio (com.roshan.artifystudio)*