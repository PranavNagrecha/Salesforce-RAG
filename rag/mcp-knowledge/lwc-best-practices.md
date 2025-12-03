# LWC Best Practices - MCP Knowledge

> This file contains knowledge extracted from Salesforce MCP Service tools.  
> It complements the lived-experience patterns in `rag/development/` and `rag/patterns/`.

## Overview

Comprehensive best practices for Lightning Web Components development, focusing on event handling, property naming, decorator usage, and component structure.

**Source**: Salesforce MCP Service - `mcp_salesforce_guide_lwc_best_practices`

## Key Patterns and Practices

### Custom Events

#### Event Creation
- Use `CustomEvent` interface for child-to-parent communication
- Dispatch events using `this.dispatchEvent()`
- For primitive data: Include directly in `detail`
- For non-primitive data: Create copies to prevent mutation
- Recommended: `{ bubbles: false, composed: false }` for maximum encapsulation

#### Event Handling
- Use declarative handling (`on{eventname}`) when possible
- For programmatic handling: Use `addEventListener()` correctly
- Remove global event listeners in `disconnectedCallback()`
- Access event data via `event.detail`

#### Event Naming
- Event names must be **lowercase only** (no camelCase or uppercase)
- Dispatched event names must not start with `on`
- Listened event names in HTML must start with `on`

### Property and Attribute Naming

#### JavaScript Properties
- Use camelCase (e.g., `itemName`, `firstName`, `maxValue`)
- Reserved prefixes: `on`, `aria`, `data`
- Reserved words: `slot`, `part`, `is`
- `@api` decorated properties follow same naming conventions

#### HTML Attributes
- Use kebab-case (dash-separated) and lowercase
- Properties starting with uppercase require `-upper` prefix in HTML
- Detect React-style attributes like `className` which should be `class` in LWC

### Decorators

#### @api Decorator
- Use only on properties and methods intended for external access
- Only one decorator per field or method
- For getters/setters: Decorate only the getter, not both
- Do not mutate `@api` properties internally

#### @track Decorator
- Only necessary for complex types (objects and arrays) when mutating properties
- Primitive values (strings, numbers, booleans) do not require `@track`
- Not needed when entire object/array is reassigned

### Lightning Message Service (LMS)

#### Message Channel Imports
- Correct pattern: `import CHANNEL_NAME from '@salesforce/messageChannel/ChannelName__c';`
- Standard channels end with `__c`
- Managed package channels include namespace

#### MessageContext Usage
- In LightningElement: Use `@wire(MessageContext)` at class level
- Not in `constructor()`, `connectedCallback()`, or `renderedCallback()`
- In service components: Use `createMessageContext()` and `releaseMessageContext()`

#### Publishing Messages
- `publish()` requires three parameters: MessageContext, MessageChannel, MessagePayload
- Payload must be JSON object (no functions or symbols)
- Cannot use in `constructor()`, `connectedCallback()`, or `renderedCallback()`

#### Subscribing to Messages
- `subscribe()` requires at least three parameters: MessageContext, MessageChannel, Listener
- Use `connectedCallback()` for subscription
- Call `unsubscribe()` in `disconnectedCallback()` if subscription returns object

### Global Value Providers (GVP)

#### Legacy GVP Usage (Deprecated)
- Legacy patterns: `$Label`, `$Resource`, `$ContentAsset`, `$User`, `$Locale`, etc.
- Must be replaced with scoped module imports

#### Valid Scoped Module Imports
- `@salesforce/label/...`
- `@salesforce/resourceUrl/...`
- `@salesforce/contentAssetUrl/...`
- `@salesforce/user/...`
- `@salesforce/i18n/...`
- `@salesforce/navigation/...`

#### Best Practices
- Use static `import` syntax for all scoped modules
- Each scoped import on its own line
- Always expose imported values through component members before using in templates
- Do not reference imported values directly in templates

### Template Directives

#### Conditional Rendering
- Use modern directives: `lwc:if`, `lwc:elseif`, `lwc:else`
- Avoid legacy: `if:true`, `if:false`
- Use only on valid elements: template tags, HTML standard tags, custom/base component tags
- Property must be bound to valid JavaScript property

#### List Rendering
- Every `for:each` must be paired with `for:item="..."`
- Use `key={item.id}` (only valid key)
- Never use index as key
- For nested loops: Use distinct `for:item` names

#### Multiple Templates
- Import multiple HTML templates in JS file
- Implement custom `render()` method
- `render()` must return imported template references, not strings

### Error Handling

#### Promise Chains
- Always include `.catch()` handlers
- Use try-catch blocks with async/await
- Handle unhandled promise rejections

#### Loading States
- Show loading indicators during wire method calls
- Include loading states for imperative Apex calls
- Provide visual feedback during async operations

#### User Feedback
- Display errors to users
- Provide actionable error messages
- Use error boundaries or error handling components

#### Wire and Apex Error Handling
- Handle `error` property in `@wire` methods
- Use `reduceErrors` method for error parsing
- Format errors for user-friendly display

### Input Validation

#### Validation Attributes
- Standard HTML inputs: `required`, `pattern`, `min`, `max`, `minlength`, `maxlength`
- Lightning Base Components: Component-specific validation attributes
- Use appropriate `type` attributes for built-in validation

#### Error Messages
- Lightning Base Components: Use `message-when-*` attributes
- Standard HTML: Use `setCustomValidity()` or associated error elements
- Clear error messages when inputs become valid

#### Submission Validation
- Use `checkValidity()` and `reportValidity()` in submission handlers
- Validate all inputs before processing
- Prevent submission if validation fails

### Rendering State Management

#### Loading States
- Use `@track isLoading` property for async operations
- Render loading state in template: `lwc:if={isLoading}`
- Reset loading state between operations

#### Error States
- Use `@track error` property for error messages
- Render error state: `lwc:elseif={error}`
- Provide error recovery mechanisms

#### Empty Data States
- Validate data arrays/objects before rendering
- Check for null/undefined before rendering
- Provide empty state messages or fallback content

### CSS Isolation

#### Proper LWC CSS
- Use `:host` for component-level styles, not component name selector
- Avoid universal selectors (`*`) that could leak
- Do not use `:host-context()` (not supported)
- Avoid ID selectors (bad practice)
- Do not override Lightning Base Component styles directly
- Do not override SLDS classes directly

#### Overuse of !important
- Avoid excessive `!important` declarations
- Use proper specificity instead
- Only use `!important` for critical overrides

### DOM Operations

#### Efficient DOM Queries
- Cache DOM queries instead of repeated calls
- Avoid DOM queries inside loops
- Batch DOM manipulations to reduce reflows

#### Performance
- Avoid unnecessary re-rendering
- Minimize forced synchronous layouts
- Optimize DOM-related performance bottlenecks

## Integration with Existing RAG

**Related Patterns**:
- [LWC Patterns](development/lwc-patterns.html) - Complements with MCP-validated practices
- [Apex Patterns](development/apex-patterns.html) - Related backend patterns
- [Error Handling](development/error-handling-and-logging.html) - Error handling patterns

**How This Complements Existing RAG**:
- Provides detailed best practices for LWC-specific patterns
- Validates event handling and component communication patterns
- Adds decorator usage guidelines
- Emphasizes proper error handling and state management

