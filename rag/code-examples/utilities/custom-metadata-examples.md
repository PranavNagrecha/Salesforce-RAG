# Custom Metadata Code Examples

> Complete, working code examples for Custom Metadata patterns.
> All examples are copy-paste ready and follow Salesforce best practices.

## Overview

Custom Metadata Types provide package-deployable configuration that can be accessed in Apex, Flows, and formulas. They're the modern approach for configuration management.

**Related Patterns**:
- [Custom Settings and Custom Metadata Patterns](development/custom-settings-metadata-patterns.html)

## Examples

### Example 1: Custom Metadata in Apex

**Pattern**: Querying and using Custom Metadata in Apex
**Use Case**: Integration endpoint configuration
**Complexity**: Basic

**Solution**:

```apex
/**
 * Utility class for accessing Custom Metadata
 */
public class IntegrationConfig {
    
    private static Map<String, Integration_Config__mdt> configMap;
    
    /**
     * Get integration configuration by name
     * @param configName Configuration name
     * @return Integration configuration
     */
    public static Integration_Config__mdt getConfig(String configName) {
        if (configMap == null) {
            loadConfigMap();
        }
        
        return configMap.get(configName);
    }
    
    /**
     * Get endpoint URL for integration
     * @param configName Configuration name
     * @return Endpoint URL
     */
    public static String getEndpoint(String configName) {
        Integration_Config__mdt config = getConfig(configName);
        return config != null ? config.Endpoint_URL__c : null;
    }
    
    /**
     * Load all configurations into map
     */
    private static void loadConfigMap() {
        configMap = new Map<String, Integration_Config__mdt>();
        
        for (Integration_Config__mdt config : [
            SELECT DeveloperName, Endpoint_URL__c, Method__c, Timeout__c
            FROM Integration_Config__mdt
            WHERE Is_Active__c = true
        ]) {
            configMap.put(config.DeveloperName, config);
        }
    }
}
```

**Explanation**:
- Query Custom Metadata via SOQL
- Cache results in static variable
- Access like regular objects
- No governor limits for queries

---

### Example 2: Custom Metadata in Flows

**Pattern**: Using Custom Metadata in Flow automation
**Use Case**: Configurable approval thresholds
**Complexity**: Basic

**Solution**:

**Flow Steps**:
1. **Get Records**: Query Custom Metadata
   - Object: `Approval_Threshold__mdt`
   - Filter: `Record_Type__c = {!$Record.RecordType.Name}`
2. **Decision**: Check threshold
   - `{!$Record.Amount} > {!Get_Threshold.Amount_Threshold__c}`
3. **Action**: Use threshold value in logic

**Explanation**:
- Query Custom Metadata via Get Records element
- Use in Flow formulas and decisions
- No DML operations
- Package-deployable

---

### Example 3: Migration from Custom Settings to Custom Metadata

**Pattern**: Migrating configuration from Custom Settings to Custom Metadata
**Use Case**: Modernizing configuration management
**Complexity**: Advanced

**Solution**:

```apex
/**
 * Migration utility for Custom Settings to Custom Metadata
 */
public class ConfigMigration {
    
    /**
     * Migrate data from Custom Settings to Custom Metadata
     * Note: Custom Metadata records must be created manually or via Metadata API
     */
    public static void migrateNotificationSettings() {
        // Get all Custom Settings records
        Map<String, Notification_Config__c> settingsMap = Notification_Config__c.getAll();
        
        // Create Custom Metadata records (via Metadata API or manual)
        // This is a simplified example - actual migration requires Metadata API
        
        for (String key : settingsMap.keySet()) {
            Notification_Config__c setting = settingsMap.get(key);
            
            // Create Custom Metadata record
            // Note: This requires Metadata API deployment
            System.debug('Migrating: ' + key + ' = ' + setting.Enable_Emails__c);
        }
    }
    
    /**
     * Update code to use Custom Metadata instead of Custom Settings
     */
    public static Boolean isEmailEnabled() {
        // Old: Notification_Config__c.getInstance().Enable_Emails__c
        // New: Query Custom Metadata
        Notification_Config_MDT__mdt config = [
            SELECT Enable_Emails__c
            FROM Notification_Config_MDT__mdt
            WHERE DeveloperName = 'Default'
            LIMIT 1
        ];
        
        return config != null && config.Enable_Emails__c == true;
    }
}
```

**Explanation**:
- Migrate data from Custom Settings to Custom Metadata
- Update code to query Custom Metadata
- Test thoroughly before removing Custom Settings

---

## Related Patterns

- [Custom Settings and Custom Metadata Patterns](development/custom-settings-metadata-patterns.html) - Complete patterns guide

