# Custom Settings Code Examples

> Complete, working code examples for Custom Settings patterns.
> All examples are copy-paste ready and follow Salesforce best practices.

## Overview

Custom Settings provide configuration data that can be accessed in Apex, Flows, and formulas. Hierarchical Custom Settings support user-level configuration, while List Custom Settings provide simple key-value lookups.

**Related Patterns**:
- [Custom Settings and Custom Metadata Patterns](../../development/custom-settings-metadata-patterns.html)

## Examples

### Example 1: Hierarchical Custom Settings Usage

**Pattern**: User-specific configuration with hierarchy
**Use Case**: User-level settings with profile/org defaults
**Complexity**: Basic

**Solution**:

```apex
/**
 * Utility class for accessing Hierarchical Custom Settings
 */
public class NotificationSettings {
    
    /**
     * Get user's email notification preference
     * Falls back to profile default, then org default
     * @return Boolean indicating if emails are enabled
     */
    public static Boolean isEmailEnabled() {
        Notification_Config__c userSetting = Notification_Config__c.getInstance();
        
        // Returns user setting, or profile default, or org default
        return userSetting.Enable_Emails__c != null ? userSetting.Enable_Emails__c : false;
    }
    
    /**
     * Get org-wide default
     * @return Boolean indicating if emails are enabled org-wide
     */
    public static Boolean isEmailEnabledOrgWide() {
        Notification_Config__c orgSetting = Notification_Config__c.getOrgDefaults();
        return orgSetting.Enable_Emails__c != null ? orgSetting.Enable_Emails__c : false;
    }
}
```

**Explanation**:
- `getInstance()` returns user-level setting with hierarchy fallback
- `getOrgDefaults()` returns org-wide default
- Hierarchy: User → Profile → Org

---

### Example 2: List Custom Settings Usage

**Pattern**: Simple key-value lookups
**Use Case**: Configuration tables or lookup data
**Complexity**: Basic

**Solution**:

```apex
/**
 * Utility class for accessing List Custom Settings
 */
public class CountryCodeLookup {
    
    private static Map<String, Country_Code__c> countryMap;
    
    /**
     * Get country name by country code
     * @param code Country code
     * @return Country name
     */
    public static String getCountryName(String code) {
        if (countryMap == null) {
            loadCountryMap();
        }
        
        Country_Code__c country = countryMap.get(code);
        return country != null ? country.Country_Name__c : null;
    }
    
    /**
     * Load all country codes into map
     */
    private static void loadCountryMap() {
        countryMap = Country_Code__c.getAll();
    }
}
```

**Explanation**:
- `getAll()` returns all records as a Map
- Cache results in static variable for performance
- Simple key-value lookups

---

## Related Patterns

- [Custom Settings and Custom Metadata Patterns](../../development/custom-settings-metadata-patterns.html) - Complete patterns guide

