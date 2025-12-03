---
layout: default
title: Platform Cache Patterns
description: Patterns for using Platform Cache to improve performance and reduce load on Salesforce and external systems
permalink: /rag/development/platform-cache-patterns.html
---

## What Was Actually Done

- Used org cache to store configuration and reference data (e.g., picklist metadata, integration endpoints) that rarely changes.
- Cached results of expensive SOQL queries for high-traffic LWCs and Flows to reduce query count and governor limit pressure.
- Implemented simple cache wrappers around `Cache.Org` and `Cache.Session` to centralize key naming and TTL (time to live).
- Used cache invalidation patterns tied to configuration changes or scheduled jobs.

## Patterns

### Pattern 1: Simple Org Cache Wrapper

**When to use**: You have read-heavy configuration or reference data shared across users.

```apex
public with sharing class OrgCacheUtil {
    private static final String CACHE_REGION = 'Default_Region';

    public static Object get(String key) {
        return Cache.Org.get(CACHE_REGION, key);
    }

    public static void put(String key, Object value, Integer ttlSeconds) {
        Cache.Org.put(CACHE_REGION, key, value, ttlSeconds);
    }
}
```

Usage:
```apex
public with sharing class ConfigService {
    private static final String PROGRAM_CONFIG_KEY = 'PROGRAM_CONFIG';

    public static Map<String, String> getProgramConfig() {
        Map<String, String> cached =
            (Map<String, String>) OrgCacheUtil.get(PROGRAM_CONFIG_KEY);
        if (cached != null) {
            return cached;
        }

        Map<String, String> config = loadProgramConfigFromCustomMetadata();
        OrgCacheUtil.put(PROGRAM_CONFIG_KEY, config, 3600);
        return config;
    }
}
```

### Pattern 2: Query Result Caching for LWCs

**When to use**: LWCs or Flows query the same data frequently and data changes infrequently.

```apex
public with sharing class ProgramSelectorService {
    private static final String CACHE_KEY = 'PROGRAM_SELECTOR_OPTIONS_V1';

    @AuraEnabled(cacheable=true)
    public static List<SelectOption> getProgramOptions() {
        List<SelectOption> cached =
            (List<SelectOption>) OrgCacheUtil.get(CACHE_KEY);
        if (cached != null) {
            return cached;
        }

        List<SelectOption> options = new List<SelectOption>();
        for (Program__c p : [
            SELECT Id, Name
            FROM Program__c
            WHERE IsActive__c = true
            ORDER BY Name
        ]) {
            options.add(new SelectOption(p.Id, p.Name));
        }

        OrgCacheUtil.put(CACHE_KEY, options, 900);
        return options;
    }
}
```

### Pattern 3: Cache Invalidation

**When to use**: Configuration changes or nightly loads should invalidate stale cache entries.

Options:
- Use a scheduled job to clear or repopulate cache nightly.
- Maintain a version key in Custom Metadata and include it in cache keys.

Example versioned key:
```apex
String version = My_Config__mdt.getInstance('GLOBAL').Cache_Version__c;
String key = 'PROGRAM_CONFIG_' + version;
```

## To Validate

- Confirm Platform Cache is licensed and enabled in the target org.
- Align region names and TTL values with actual org configuration.


