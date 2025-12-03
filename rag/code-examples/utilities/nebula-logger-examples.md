---
layout: default
title: Nebula Logger Code Examples
description: Examples for using the Nebula Logger open-source library for structured logging in Salesforce
permalink: /rag/code-examples/utilities/nebula-logger-examples.html
---

## What Was Actually Done

- Adopted Nebula Logger as the standard logging framework for complex Apex services and triggers.
- Used the provided `Logger` API to capture context, log levels, and structured data instead of raw `System.debug`.
- Integrated Nebula Logger with asynchronous jobs and callouts to correlate logs across transactions.

## Basic Usage

```apex
public with sharing class ExampleService {
    public static void doWork() {
        Logger.info('Starting ExampleService.doWork');

        try {
            // Business logic
            Logger.debug('About to query contacts');
            List<Contact> contacts = [
                SELECT Id, LastName
                FROM Contact
                LIMIT 10
            ];
            Logger.info('Loaded contacts', new Map<String, Object>{
                'count' => contacts.size()
            });
        } catch (Exception e) {
            Logger.error('Error in ExampleService.doWork', e);
            throw e;
        }
    }
}
```

## To Validate

- Confirm the Nebula Logger managed package or source is installed and configured in the target org.
- Align log retention and log level configuration with org logging strategy.


