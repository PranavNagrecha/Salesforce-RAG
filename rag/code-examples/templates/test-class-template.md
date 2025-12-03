---
layout: default
title: Test Class Template
description: Code examples for Test Class Template
permalink: /rag/code-examples/templates/test-class-template.html
---

# Test Class Template

**Use Case**: Basic test class with test data factory and assertions

**Template**:
```apex
/**
 * Test class for [ClassName]
 * Tests all public methods with positive and negative test cases
 */
@isTest
private class [ClassName]Test {
    
    /**
     * Test data factory method
     * @return List of test [ObjectName] records
     */
    private static List<[ObjectName]> createTest[ObjectName]s(Integer count) {
        List<[ObjectName]> records = new List<[ObjectName]>();
        
        for (Integer i = 0; i < count; i++) {
            records.add(new [ObjectName](
                Name = 'Test ' + i,
                // Add other required fields
            ));
        }
        
        return records;
    }
    
    /**
     * Test [methodName] - Success scenario
     */
    @isTest
    static void test[MethodName]_Success() {
        // Create test data
        List<[ObjectName]> testRecords = createTest[ObjectName]s(2);
        insert testRecords;
        
        Set<Id> recordIds = new Set<Id>();
        for ([ObjectName] record : testRecords) {
            recordIds.add(record.Id);
        }
        
        Test.startTest();
        [ReturnType] result = [ClassName].[methodName]([parameters]);
        Test.stopTest();
        
        // Verify results
        System.assertNotEquals(null, result, 'Result should not be null');
        // Add more assertions
    }
    
    /**
     * Test [methodName] - Error scenario
     */
    @isTest
    static void test[MethodName]_Error() {
        // Create test data that will cause error
        // Or use invalid input
        
        Test.startTest();
        try {
            [ClassName].[methodName]([invalidParameters]);
            System.assert(false, 'Should throw exception');
        } catch ([ExceptionType] e) {
            System.assert(e.getMessage().contains('[expectedError]'), 'Should throw appropriate error');
        }
        Test.stopTest();
    }
    
    /**
     * Test [methodName] - Bulk scenario
     */
    @isTest
    static void test[MethodName]_Bulk() {
        // Create bulk test data (200+ records)
        List<[ObjectName]> testRecords = createTest[ObjectName]s(200);
        insert testRecords;
        
        Set<Id> recordIds = new Set<Id>();
        for ([ObjectName] record : testRecords) {
            recordIds.add(record.Id);
        }
        
        Test.startTest();
        [ReturnType] result = [ClassName].[methodName]([parameters]);
        Test.stopTest();
        
        // Verify bulk processing
        System.assertEquals(200, result.size(), 'Should process all 200 records');
    }
}
```

**Customization Points**:
- Replace `[ClassName]` with actual class name
- Replace `[ObjectName]` with actual object name
- Replace `[methodName]` with actual method name
- Replace `[ReturnType]` with actual return type
- Replace `[parameters]` with actual parameters
- Replace `[ExceptionType]` with actual exception type
- Replace `[expectedError]` with expected error message
- Add test data factory methods
- Add more test scenarios

**Best Practices**:
- Use `@isTest` annotation
- Use `Test.startTest()` and `Test.stopTest()`
- Test with bulk data (200+ records)
- Include positive and negative test cases
- Use test data factories
- Include assertions
- Test error scenarios
- Avoid `@SeeAllData` annotation

**Related Patterns**:
- <a href="{{ '/rag/development/apex-patterns.html' | relative_url }}">Apex Patterns</a> - Testing strategies
- <a href="{{ '/rag/code-examples/templates/project-methods/testing-strategy.html' | relative_url }}">Testing Strategy</a> - Testing best practices

