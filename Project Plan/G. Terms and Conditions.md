
# Artify Studio - Terms and Conditions

## 1. Legal Framework and Compliance

### 1.1 Terms of Service Architecture

#### Comprehensive Legal Documentation
```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Terms and Conditions Framework                       │
├─────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │
│  │   End User  │  │   Developer │  │   Enterprise│  │   Platform  │    │
│  │   License   │  │   Agreement │  │   Agreement │  │   Terms     │    │
│  │ Agreement   │  │             │  │             │  │             │    │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘    │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │
│  │ • Usage     │  │ • API       │  │ • Commercial│  │ • App Store │    │
│  │ • Rights    │  │ • Access    │  │ • License   │  │ • Terms     │    │
│  │ • Privacy   │  │ • Integration│  │ • Support   │  │ • Compliance│    │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘    │
├─────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │
│  │ Privacy     │  │   Data      │  │   Content   │  │   Intellectual│    │
│  │  Policy     │  │ Processing  │  │   Policy    │  │   Property   │    │
│  │             │  │   Agreement │  │             │  │   Rights     │    │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘    │
└─────────────────────────────────────────────────────────────────────────┘
```

### 1.2 Legal Document Matrix

| Document Type | Purpose | Audience | Enforcement | Update Frequency |
|---------------|---------|----------|-------------|------------------|
| **End User License Agreement** | Define user rights and restrictions | All users | Legal contract | Major releases |
| **Privacy Policy** | Data collection and usage disclosure | All users | Legal requirement | As needed |
| **Terms of Service** | Service usage terms and conditions | All users | Legal contract | Annually |
| **Developer Agreement** | API and SDK usage terms | Developers | Legal contract | Major releases |
| **Enterprise Agreement** | Commercial licensing terms | Business users | Legal contract | As needed |
| **Platform Terms** | App store compliance terms | Platform users | Platform requirement | Platform changes |

## 2. End User License Agreement (EULA)

### 2.1 User Rights and Permissions

#### Comprehensive Usage Rights Framework
```python
# src/legal/eula_framework.py
from typing import Dict, Any, List, Optional
from enum import Enum
from dataclasses import dataclass

class LicenseType(Enum):
    """Types of software licenses"""
    FREEWARE = "freeware"
    FREEMIUM = "freemium"
    PREMIUM = "premium"
    ENTERPRISE = "enterprise"
    TRIAL = "trial"
    EDUCATIONAL = "educational"

class UsageRights(Enum):
    """User usage rights"""
    PERSONAL_USE = "personal_use"
    COMMERCIAL_USE = "commercial_use"
    EDUCATIONAL_USE = "educational_use"
    NON_COMMERCIAL_USE = "non_commercial_use"
    INTERNAL_BUSINESS_USE = "internal_business_use"

@dataclass
class LicenseGrant:
    """License grant specification"""
    license_type: LicenseType
    granted_rights: List[UsageRights]
    limitations: List[str]
    territory: str
    duration: str
    renewal_terms: str

class EULAManager:
    """Manages End User License Agreement compliance"""

    def __init__(self):
        self.license_grants = self._initialize_license_grants()
        self.usage_tracking = self._initialize_usage_tracking()

    def _initialize_license_grants(self) -> Dict[str, LicenseGrant]:
        """Initialize license grants for different user types"""
        return {
            'free_user': LicenseGrant(
                license_type=LicenseType.FREEWARE,
                granted_rights=[UsageRights.PERSONAL_USE, UsageRights.NON_COMMERCIAL_USE],
                limitations=[
                    'Maximum 10 transformations per day',
                    'Standard export quality only',
                    'No batch processing',
                    'No API access',
                    'No priority support'
                ],
                territory='Worldwide',
                duration='Perpetual (with ongoing access to free features)',
                renewal_terms='Automatic renewal of free access'
            ),
            'premium_user': LicenseGrant(
                license_type=LicenseType.FREEMIUM,
                granted_rights=[
                    UsageRights.PERSONAL_USE,
                    UsageRights.NON_COMMERCIAL_USE,
                    UsageRights.EDUCATIONAL_USE
                ],
                limitations=[
                    'Maximum 100 transformations per day',
                    'High export quality',
                    'Batch processing enabled',
                    'Email support',
                    'No commercial use rights'
                ],
                territory='Worldwide',
                duration='Subscription period',
                renewal_terms='Automatic renewal unless cancelled'
            ),
            'enterprise_user': LicenseGrant(
                license_type=LicenseType.ENTERPRISE,
                granted_rights=[
                    UsageRights.PERSONAL_USE,
                    UsageRights.COMMERCIAL_USE,
                    UsageRights.INTERNAL_BUSINESS_USE,
                    UsageRights.EDUCATIONAL_USE
                ],
                limitations=[
                    'Unlimited transformations',
                    'Maximum export quality',
                    'Full batch processing',
                    'API access included',
                    'Priority support',
                    'Custom integrations'
                ],
                territory='Worldwide',
                duration='Subscription period',
                renewal_terms='Annual renewal required'
            )
        }

    def _initialize_usage_tracking(self) -> Dict[str, Dict[str, Any]]:
        """Initialize usage tracking for license compliance"""
        return {
            'free_tier': {
                'daily_transformation_limit': 10,
                'export_quality_limit': 85,
                'feature_restrictions': ['batch_processing', 'api_access'],
                'support_level': 'community_only'
            },
            'premium_tier': {
                'daily_transformation_limit': 100,
                'export_quality_limit': 100,
                'allowed_features': ['batch_processing', 'priority_support'],
                'support_level': 'email_support'
            },
            'enterprise_tier': {
                'daily_transformation_limit': -1,  # Unlimited
                'export_quality_limit': 100,
                'allowed_features': ['batch_processing', 'api_access', 'custom_integrations'],
                'support_level': 'priority_support'
            }
        }

    def validate_license_compliance(self, user_id: str, action: str,
                                  context: Dict[str, Any]) -> Dict[str, Any]:
        """Validate user action against license terms"""
        try:
            # Get user license information
            user_license = self._get_user_license_info(user_id, context)

            # Check if action is permitted under license
            action_permitted = self._check_action_permission(action, user_license, context)

            if not action_permitted['permitted']:
                return {
                    'license_compliant': False,
                    'violation_type': 'license_restriction',
                    'violation_details': action_permitted['reason'],
                    'upgrade_required': self._check_upgrade_required(action, user_license),
                    'upgrade_suggestions': self._get_upgrade_suggestions(action, user_license)
                }

            # Check usage limits
            usage_compliant = self._check_usage_limits(user_id, action, user_license, context)

            if not usage_compliant['compliant']:
                return {
                    'license_compliant': False,
                    'violation_type': 'usage_limit_exceeded',
                    'violation_details': usage_compliant['violation'],
                    'limit_reset_info': usage_compliant['reset_info'],
                    'grace_period_available': usage_compliant['grace_period']
                }

            # License is compliant
            return {
                'license_compliant': True,
                'license_type': user_license['license_type'],
                'remaining_usage': self._calculate_remaining_usage(user_id, user_license),
                'license_expiry': user_license.get('expiry_date'),
                'upgrade_available': self._check_upgrade_available(user_license)
            }

        except Exception as e:
            return {
                'license_compliant': False,
                'error': f'License validation failed: {str(e)}',
                'fallback_action': 'restrict_access'
            }

    def _get_user_license_info(self, user_id: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Get user's license information"""
        # Implementation would query user database
        user_plan = context.get('user_plan', 'free')

        return {
            'user_id': user_id,
            'license_type': user_plan,
            'grant_date': '2025-01-01',
            'expiry_date': None if user_plan == 'free' else '2025-12-31',
            'auto_renewal': user_plan != 'free',
            'license_grant': self.license_grants.get(f'{user_plan}_user')
        }

    def _check_action_permission(self, action: str, user_license: Dict[str, Any],
                               context: Dict[str, Any]) -> Dict[str, Any]:
        """Check if action is permitted under user's license"""
        license_grant = user_license.get('license_grant')

        if not license_grant:
            return {
                'permitted': False,
                'reason': 'No valid license grant found'
            }

        # Check if action requires specific rights
        action_rights_required = self._get_action_rights_required(action)

        # Check if user's license grants required rights
        user_rights = set(license_grant.granted_rights)
        required_rights = set(action_rights_required)

        if not required_rights.issubset(user_rights):
            missing_rights = required_rights - user_rights
            return {
                'permitted': False,
                'reason': f'License does not grant required rights: {missing_rights}'
            }

        return {
            'permitted': True,
            'reason': 'Action permitted under license'
        }

    def _get_action_rights_required(self, action: str) -> List[UsageRights]:
        """Get rights required for specific action"""
        action_rights_map = {
            'process_transformation': [UsageRights.PERSONAL_USE],
            'export_commercial': [UsageRights.COMMERCIAL_USE],
            'batch_process': [UsageRights.COMMERCIAL_USE],
            'api_access': [UsageRights.COMMERCIAL_USE],
            'educational_use': [UsageRights.EDUCATIONAL_USE]
        }

        return action_rights_map.get(action, [UsageRights.PERSONAL_USE])

    def _check_usage_limits(self, user_id: str, action: str, user_license: Dict[str, Any],
                          context: Dict[str, Any]) -> Dict[str, Any]:
        """Check usage limits compliance"""
        license_type = user_license.get('license_type', 'free')
        usage_limits = self.usage_tracking.get(f'{license_type}_tier', {})

        # Check daily transformation limit
        if action == 'process_transformation':
            daily_limit = usage_limits.get('daily_transformation_limit', 10)
            current_usage = self._get_current_daily_usage(user_id)

            if daily_limit != -1 and current_usage >= daily_limit:
                return {
                    'compliant': False,
                    'violation': f'Daily transformation limit exceeded ({current_usage}/{daily_limit})',
                    'reset_info': 'Limits reset daily at midnight UTC',
                    'grace_period': False
                }

        # Check feature restrictions
        restricted_features = usage_limits.get('feature_restrictions', [])
        if action in restricted_features:
            return {
                'compliant': False,
                'violation': f'Feature {action} not available in current plan',
                'reset_info': 'Feature available in higher tier plans',
                'grace_period': False
            }

        return {
            'compliant': True,
            'violation': None,
            'reset_info': None,
            'grace_period': False
        }

    def _get_current_daily_usage(self, user_id: str) -> int:
        """Get current daily usage for user"""
        # Implementation would query usage database
        return 5  # Placeholder

    def _calculate_remaining_usage(self, user_id: str, user_license: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate remaining usage under license"""
        license_type = user_license.get('license_type', 'free')
        usage_limits = self.usage_tracking.get(f'{license_type}_tier', {})

        daily_limit = usage_limits.get('daily_transformation_limit', 10)
        current_usage = self._get_current_daily_usage(user_id)

        remaining = daily_limit - current_usage if daily_limit != -1 else -1

        return {
            'daily_transformations_remaining': max(0, remaining),
            'unlimited_usage': remaining == -1,
            'reset_time': 'midnight_utc',
            'usage_period': 'daily'
        }

    def _check_upgrade_required(self, action: str, user_license: Dict[str, Any]) -> bool:
        """Check if upgrade is required for action"""
        license_type = user_license.get('license_type', 'free')

        # Define upgrade requirements
        upgrade_required_actions = {
            'free': ['batch_processing', 'api_access', 'commercial_use'],
            'premium': ['api_access', 'commercial_use'],
            'enterprise': []  # No upgrades needed
        }

        return action in upgrade_required_actions.get(license_type, [])

    def _get_upgrade_suggestions(self, action: str, user_license: Dict[str, Any]) -> List[str]:
        """Get upgrade suggestions for restricted action"""
        current_license = user_license.get('license_type', 'free')

        suggestions = []

        if current_license == 'free':
            suggestions.append("Upgrade to Premium for batch processing and higher limits")
            suggestions.append("Upgrade to Enterprise for commercial use and API access")
        elif current_license == 'premium':
            suggestions.append("Upgrade to Enterprise for API access and commercial licensing")

        return suggestions

    def _check_upgrade_available(self, user_license: Dict[str, Any]) -> bool:
        """Check if license upgrade is available"""
        current_license = user_license.get('license_type', 'free')

        # All licenses except enterprise have upgrade paths
        return current_license != 'enterprise'

    def generate_license_summary(self, user_id: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive license summary"""
        user_license = self._get_user_license_info(user_id, context)

        return {
            'license_type': user_license['license_type'],
            'license_grant': user_license['license_grant'],
            'current_usage': self._get_current_usage_summary(user_id),
            'remaining_allowances': self._calculate_remaining_usage(user_id, user_license),
            'upgrade_options': self._get_available_upgrades(user_license),
            'license_compliance_status': 'active',
            'next_renewal_date': user_license.get('expiry_date'),
            'support_level': self._get_support_level(user_license)
        }

    def _get_current_usage_summary(self, user_id: str) -> Dict[str, Any]:
        """Get current usage summary for user"""
        return {
            'today_transformations': self._get_current_daily_usage(user_id),
            'monthly_transformations': 150,  # Would be calculated
            'storage_used_mb': 45,  # Would be calculated
            'last_activity': '2025-10-19T10:30:00Z'
        }

    def _get_available_upgrades(self, user_license: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get available license upgrades"""
        current_license = user_license.get('license_type', 'free')

        upgrades = []

        if current_license == 'free':
            upgrades.append({
                'target_license': 'premium',
                'price_monthly': 9.99,
                'price_yearly': 99.99,
                'features_added': ['Batch processing', 'Higher quality', 'Priority support'],
                'savings_yearly': '17%'
            })
            upgrades.append({
                'target_license': 'enterprise',
                'price_monthly': 29.99,
                'price_yearly': 299.99,
                'features_added': ['API access', 'Commercial license', 'Custom integrations'],
                'savings_yearly': '17%'
            })

        elif current_license == 'premium':
            upgrades.append({
                'target_license': 'enterprise',
                'price_monthly': 29.99,
                'price_yearly': 299.99,
                'features_added': ['API access', 'Commercial license'],
                'savings_yearly': '17%'
            })

        return upgrades

    def _get_support_level(self, user_license: Dict[str, Any]) -> str:
        """Get support level for license"""
        license_type = user_license.get('license_type', 'free')

        support_levels = {
            'free': 'Community support only',
            'premium': 'Email support',
            'enterprise': 'Priority phone and email support'
        }

        return support_levels.get(license_type, 'Community support only')

    def handle_license_violation(self, violation: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle license violation"""
        violation_type = violation.get('violation_type', 'unknown')

        if violation_type == 'license_restriction':
            return self._handle_license_restriction_violation(violation, context)
        elif violation_type == 'usage_limit_exceeded':
            return self._handle_usage_limit_violation(violation, context)
        else:
            return self._handle_generic_violation(violation, context)

    def _handle_license_restriction_violation(self, violation: Dict[str, Any],
                                            context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle license restriction violation"""
        return {
            'violation_handled': True,
            'user_action_required': True,
            'notification_type': 'license_upgrade_required',
            'notification_message': 'This feature requires a higher license tier',
            'upgrade_options': violation.get('upgrade_suggestions', []),
            'graceful_degradation': 'disable_feature'
        }

    def _handle_usage_limit_violation(self, violation: Dict[str, Any],
                                    context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle usage limit violation"""
        return {
            'violation_handled': True,
            'user_action_required': False,
            'notification_type': 'usage_limit_reached',
            'notification_message': 'Daily usage limit reached',
            'limit_reset_info': violation.get('limit_reset_info'),
            'graceful_degradation': 'disable_action'
        }

    def _handle_generic_violation(self, violation: Dict[str, Any],
                                 context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle generic license violation"""
        return {
            'violation_handled': True,
            'user_action_required': True,
            'notification_type': 'license_issue',
            'notification_message': 'License compliance issue detected',
            'contact_support': True
        }

    def get_license_analytics(self) -> Dict[str, Any]:
        """Get license compliance analytics"""
        return {
            'total_licenses_issued': 10000,
            'active_licenses': 8500,
            'license_compliance_rate': 96.0,
            'most_common_violations': ['usage_limits', 'feature_restrictions'],
            'upgrade_conversion_rate': 12.0,
            'churn_rate': 3.0
        }
```

### 2.2 Privacy Policy and Data Handling

#### Comprehensive Privacy Framework
```python
# src/legal/privacy_framework.py
from typing import Dict, Any, List, Optional
from enum import Enum

class DataCategory(Enum):
    """Categories of collected data"""
    PERSONAL_INFORMATION = "personal_information"
    USAGE_DATA = "usage_data"
    DEVICE_INFORMATION = "device_information"
    CONTENT_DATA = "content_data"
    ANALYTICS_DATA = "analytics_data"
    PREFERENCE_DATA = "preference_data"

class DataProcessingPurpose(Enum):
    """Purposes for data processing"""
    SERVICE_PROVISION = "service_provision"
    PERFORMANCE_IMPROVEMENT = "performance_improvement"
    USER_EXPERIENCE = "user_experience"
    SECURITY = "security"
    LEGAL_COMPLIANCE = "legal_compliance"
    MARKETING = "marketing"

class PrivacyPolicyManager:
    """Manages privacy policy compliance"""

    def __init__(self):
        self.data_collection_rules = self._initialize_data_collection_rules()
        self.privacy_standards = self._initialize_privacy_standards()

    def _initialize_data_collection_rules(self) -> Dict[str, Dict[str, Any]]:
        """Initialize data collection rules"""
        return {
            'personal_information': {
                'collection_method': 'user_provided',
                'storage_duration': 'until_account_deletion',
                'sharing_allowed': False,
                'encryption_required': True,
                'access_logging': True,
                'purpose': [DataProcessingPurpose.SERVICE_PROVISION, DataProcessingPurpose.LEGAL_COMPLIANCE]
            },
            'usage_data': {
                'collection_method': 'automatically_collected',
                'storage_duration': '13_months',
                'sharing_allowed': True,
                'encryption_required': False,
                'access_logging': True,
                'purpose': [
                    DataProcessingPurpose.PERFORMANCE_IMPROVEMENT,
                    DataProcessingPurpose.USER_EXPERIENCE,
                    DataProcessingPurpose.ANALYTICS_DATA
                ]
            },
            'device_information': {
                'collection_method': 'automatically_collected',
                'storage_duration': 'session_only',
                'sharing_allowed': False,
                'encryption_required': False,
                'access_logging': False,
                'purpose': [DataProcessingPurpose.SERVICE_PROVISION, DataProcessingPurpose.SECURITY]
            },
            'content_data': {
                'collection_method': 'user_generated',
                'storage_duration': 'until_user_deletion',
                'sharing_allowed': False,
                'encryption_required': True,
                'access_logging': True,
                'purpose': [DataProcessingPurpose.SERVICE_PROVISION]
            }
        }

    def _initialize_privacy_standards(self) -> Dict[str, List[str]]:
        """Initialize privacy standards compliance"""
        return {
            'gdpr_compliance': [
                'Data minimization principle',
                'Purpose limitation principle',
                'Storage limitation principle',
                'Data subject rights implementation',
                'Privacy by design',
                'Data protection impact assessments'
            ],
            'ccpa_compliance': [
                'Right to know about data collection',
                'Right to delete personal information',
                'Right to opt-out of data sales',
                'Right to non-discrimination',
                'Clear privacy policy',
                'Data broker registration'
            ],
            'app_store_compliance': [
                'Privacy policy accessibility',
                'Data collection disclosure',
                'Third-party SDK disclosure',
                'Permission justification',
                'Data retention transparency'
            ]
        }

    def validate_privacy_compliance(self, data_operation: str, data_category: DataCategory,
                                  context: Dict[str, Any]) -> Dict[str, Any]:
        """Validate privacy compliance for data operation"""
        try:
            # Get data collection rules for category
            category_rules = self.data_collection_rules.get(data_category.value)

            if not category_rules:
                return {
                    'privacy_compliant': False,
                    'error': f'Unknown data category: {data_category}'
                }

            # Check if operation is allowed
            operation_allowed = self._check_operation_permission(data_operation, category_rules, context)

            if not operation_allowed['allowed']:
                return {
                    'privacy_compliant': False,
                    'violation': operation_allowed['reason'],
                    'remediation': operation_allowed['remediation']
                }

            # Validate data processing purpose
            purpose_valid = self._validate_processing_purpose(data_operation, data_category, context)

            if not purpose_valid['valid']:
                return {
                    'privacy_compliant': False,
                    'violation': purpose_valid['violation'],
                    'legal_basis_required': purpose_valid['legal_basis']
                }

            # Check data retention compliance
            retention_compliant = self._check_retention_compliance(data_category, context)

            return {
                'privacy_compliant': True,
                'data_category': data_category.value,
                'collection_rules': category_rules,
                'processing_purpose': purpose_valid['purpose'],
                'retention_compliant': retention_compliant,
                'consent_status': self._get_consent_status(data_category, context),
                'data_subject_rights': self._get_applicable_rights(data_category)
            }

        except Exception as e:
            return {
                'privacy_compliant': False,
                'error': f'Privacy validation failed: {str(e)}'
            }

    def _check_operation_permission(self, operation: str, rules: Dict[str, Any],
                                  context: Dict[str, Any]) -> Dict[str, Any]:
        """Check if data operation is permitted"""
        # Define allowed operations per data category
        allowed_operations = {
            'personal_information': ['collect', 'store', 'process'],
            'usage_data': ['collect', 'analyze', 'aggregate'],
            'device_information': ['collect', 'use'],
            'content_data': ['store', 'process', 'delete']
        }

        category_key = list(allowed_operations.keys())[0]  # Simplified
        permitted_operations = allowed_operations.get(category_key, [])

        if operation not in permitted_operations:
            return {
                'allowed': False,
                'reason': f'Operation {operation} not permitted for this data category',
                'remediation': 'Review data processing permissions'
            }

        return {
            'allowed': True,
            'reason': 'Operation permitted under privacy rules'
        }

    def _validate_processing_purpose(self, operation: str, data_category: DataCategory,
                                   context: Dict[str, Any]) -> Dict[str, Any]:
        """Validate data processing purpose"""
        category_rules = self.data_collection_rules.get(data_category.value, {})
        allowed_purposes = category_rules.get('purpose', [])

        # Map operation to purpose
        operation_purpose_map = {
            'collect': DataProcessingPurpose.SERVICE_PROVISION,
            'analyze': DataProcessingPurpose.PERFORMANCE_IMPROVEMENT,
            'store': DataProcessingPurpose.SERVICE_PROVISION,
            'share': DataProcessingPurpose.MARKETING
        }

        operation_purpose = operation_purpose_map.get(operation, DataProcessingPurpose.SERVICE_PROVISION)

        if operation_purpose not in allowed_purposes:
            return {
                'valid': False,
                'violation': f'Processing purpose {operation_purpose.value} not allowed for {data_category.value}',
                'legal_basis': self._get_legal_basis_requirement(operation_purpose)
            }

        return {
            'valid': True,
            'purpose': operation_purpose.value
        }

    def _get_legal_basis_requirement(self, purpose: DataProcessingPurpose) -> str:
        """Get legal basis requirement for processing purpose"""
        legal_bases = {
            DataProcessingPurpose.SERVICE_PROVISION: 'Contract necessity',
            DataProcessingPurpose.PERFORMANCE_IMPROVEMENT: 'Legitimate interest',
            DataProcessingPurpose.USER_EXPERIENCE: 'Consent',
            DataProcessingPurpose.SECURITY: 'Legal obligation',
            DataProcessingPurpose.LEGAL_COMPLIANCE: 'Legal obligation',
            DataProcessingPurpose.MARKETING: 'Consent'
        }

        return legal_bases.get(purpose, 'Consent')

    def _check_retention_compliance(self, data_category: DataCategory,
                                  context: Dict[str, Any]) -> bool:
        """Check data retention compliance"""
        category_rules = self.data_collection_rules.get(data_category.value, {})
        max_retention = category_rules.get('storage_duration', 'session_only')

        # Check if data has exceeded retention period
        data_age = context.get('data_age_days', 0)

        if max_retention == 'session_only':
            return data_age == 0  # Must be deleted after session
        elif max_retention == '13_months':
            return data_age <= 395  # 13 months in days
        elif max_retention == 'until_account_deletion':
            return context.get('account_active', True)
        elif max_retention == 'until_user_deletion':
            return context.get('user_consent_active', True)

        return True

    def _get_consent_status(self, data_category: DataCategory, context: Dict[str, Any]) -> Dict[str, Any]:
        """Get consent status for data category"""
        user_consent = context.get('user_consent', {})

        return {
            'consent_obtained': user_consent.get(f'{data_category.value}_consent', False),
            'consent_timestamp': user_consent.get(f'{data_category.value}_consent_date'),
            'consent_version': user_consent.get(f'{data_category.value}_consent_version', '1.0'),
            'withdrawal_available': True,
            'consent_expiry': self._calculate_consent_expiry(data_category)
        }

    def _calculate_consent_expiry(self, data_category: DataCategory) -> Optional[str]:
        """Calculate when consent expires"""
        expiry_periods = {
            DataCategory.PERSONAL_INFORMATION: 'until_withdrawal',
            DataCategory.USAGE_DATA: '13_months',
            DataCategory.DEVICE_INFORMATION: 'session',
            DataCategory.CONTENT_DATA: 'until_deletion',
            DataCategory.ANALYTICS_DATA: '13_months',
            DataCategory.PREFERENCE_DATA: 'until_withdrawal'
        }

        return expiry_periods.get(data_category, 'session')

    def _get_applicable_rights(self, data_category: DataCategory) -> List[str]:
        """Get data subject rights applicable to category"""
        rights_map = {
            DataCategory.PERSONAL_INFORMATION: [
                'Right of access',
                'Right to rectification',
                'Right to erasure',
                'Right to data portability',
                'Right to object',
                'Right to withdraw consent'
            ],
            DataCategory.USAGE_DATA: [
                'Right of access',
                'Right to erasure',
                'Right to object'
            ],
            DataCategory.DEVICE_INFORMATION: [
                'Right of access',
                'Right to erasure'
            ],
            DataCategory.CONTENT_DATA: [
                'Right of access',
                'Right to rectification',
