---
title: "Accurately Estimating Salesforce Project Work"
source: "The Salesforce Master Class wiki"
source_url: "https://github.com/Coding-With-The-Force/The-Salesforce-Master-Class/wiki"
topic: "Topic 4: The Complete Guide To Salesforce Architecture"
section: "How to Accurately Estimate Project Work"
level: "Advanced"
tags:
  - salesforce
  - architecture
  - estimation
  - project-management
  - best-practices
last_reviewed: "2025-01-XX"
---

# Overview

Accurate project estimation is critical for setting realistic expectations, managing stakeholder relationships, and delivering successful Salesforce implementations. Estimation requires understanding all project components, accounting for hidden work, and using appropriate estimation techniques.

Project estimation encompasses identifying all work components (not just development), accounting for different team roles, estimating to median talent rather than expert skill, estimating lowest-cost OOTB options first, and managing unrealistic expectations. Effective estimation prevents scope creep, manages stakeholder expectations, and enables successful delivery.

Estimation is both art and science: it requires technical understanding, experience with similar projects, and ability to account for unknowns. Good estimates are realistic, not optimistic, and include appropriate buffers for uncertainty.

# Core Concepts

## What Project Work Estimation Is

**What it is**: Process of predicting the effort, time, and resources required to complete a project or work item.

**Key components**:
- **Effort estimation**: How much work is required (person-hours, story points)
- **Time estimation**: How long it will take (calendar time)
- **Resource estimation**: What resources are needed (developers, admins, testers)
- **Cost estimation**: What it will cost (labor, licenses, tools)

**Estimation challenges**:
- Requirements are often incomplete or unclear
- Unknown technical challenges may arise
- Dependencies on other teams or systems
- Changing requirements during project
- Team velocity varies

## The Many Roles on a Team

**What it is**: Projects require multiple roles, not just developers. Each role contributes to project success and must be accounted for in estimates.

**Key roles and their contributions**:
- **Architects**: Design, architecture decisions, technical guidance
- **Developers**: Code development, unit testing, technical implementation
- **Administrators**: Configuration, declarative setup, user management
- **Business Analysts**: Requirements gathering, process documentation, user stories
- **Testers**: Test planning, test execution, bug reporting
- **Project Managers**: Coordination, communication, risk management
- **Trainers**: Training material creation, training delivery
- **Documentation**: Technical documentation, user guides

**Why it matters**: Estimating only development time misses significant portions of project work. All roles contribute to timeline and must be included.

**Estimation approach**: Break down work by role, estimate each role's contribution, account for coordination overhead between roles.

## Guarding Against Unrealistic Expectations

**What it is**: Techniques for managing stakeholder expectations and preventing commitment to unrealistic timelines or scope.

**Common unrealistic expectations**:
- "Can't you just add a field?" (underestimating complexity)
- "It's just configuration" (ignoring testing, training, change management)
- "We need it next week" (ignoring dependencies and process)
- "It should be simple" (assuming simplicity without understanding)

**Guarding techniques**:
- **Break down work**: Show all components, not just visible ones
- **Explain dependencies**: What must happen before this can start?
- **Provide ranges**: "2-4 weeks" not "3 weeks" when uncertain
- **Estimate to median talent**: Not your own expert skill level
- **Include all phases**: Design, development, testing, deployment, training
- **Account for unknowns**: Buffer for unexpected challenges

## Estimating Lowest-Cost OOTB Option First

**What it is**: Estimate the simplest, most cost-effective out-of-the-box solution first, then show cost of enhancements.

**Why it matters**: Stakeholders need to understand baseline cost before deciding on enhancements. Starting with ideal solution sets wrong expectations.

**Estimation approach**:
1. **OOTB baseline**: Estimate simplest solution using standard Salesforce features
2. **Enhancement options**: Show cost of each enhancement (declarative customization, custom development)
3. **Tradeoff communication**: "OOTB is $X and takes Y weeks. Adding feature Z adds $A and B weeks."
4. **Decision support**: Enable stakeholders to make informed tradeoff decisions

**Example**: Instead of estimating custom portal with all features, estimate standard Experience Cloud site first, then show cost of each custom feature.

## Estimating to Median Talent, Not Your Own Skills

**What it is**: Estimate based on average developer capability, not your own expert-level skills.

**Why it matters**: You may be able to do something quickly, but typical team members may take longer. Estimates should reflect team capability, not individual expertise.

**Estimation approach**:
- Consider team's average skill level
- Account for learning curve if using new technologies
- Include time for code reviews and revisions
- Don't assume everyone has your depth of knowledge
- Provide estimates that team can actually achieve

**Example**: You might build a complex Flow in 2 hours, but estimate 1 day for median developer who needs to understand requirements, design flow, test, and get review.

## Solving Work from Broken and Scattered Requirements

**What it is**: Techniques for estimating when requirements are incomplete, unclear, or contradictory.

**Common requirement problems**:
- Requirements are vague ("make it better")
- Requirements conflict with each other
- Requirements are incomplete (missing edge cases)
- Requirements change frequently
- Requirements don't account for platform constraints

**Estimation approach**:
- **Clarify first**: Don't estimate unclear requirements. Ask questions, get clarification.
- **Document assumptions**: State assumptions explicitly in estimate
- **Provide ranges**: Use wider ranges when requirements are uncertain
- **Phase approach**: Estimate discovery phase first, then implementation
- **Buffer for changes**: Include time for requirement clarification and changes

# Deep-Dive Patterns & Best Practices

## Estimation Techniques

### Bottom-Up Estimation

**What it is**: Break work into small tasks, estimate each task, sum for total estimate.

**When to use**: When work is well-understood and can be broken down.

**Advantages**: More accurate, accounts for all work components.

**Disadvantages**: Time-consuming, may miss integration overhead.

### Top-Down Estimation

**What it is**: Estimate overall effort based on similar past projects, then break down.

**When to use**: Early in project when details are unclear, or for similar work.

**Advantages**: Fast, good for high-level planning.

**Disadvantages**: Less accurate, may miss unique aspects.

### Three-Point Estimation

**What it is**: Provide optimistic, pessimistic, and most likely estimates, calculate weighted average.

**Formula**: (Optimistic + 4×Most Likely + Pessimistic) / 6

**When to use**: When there's significant uncertainty.

**Advantages**: Accounts for uncertainty, provides range.

**Disadvantages**: Requires understanding of best/worst case scenarios.

### Story Points

**What it is**: Relative sizing using points (1, 2, 3, 5, 8, 13) rather than hours.

**When to use**: Agile teams with established velocity.

**Advantages**: Focuses on relative complexity, not absolute time.

**Disadvantages**: Requires team calibration and velocity tracking.

## Accounting for Hidden Work

**What it is**: Work that's necessary but not obvious in initial requirements.

**Common hidden work**:
- **Requirements clarification**: Time spent understanding what's really needed
- **Design and architecture**: Time to design solution before building
- **Testing**: Unit tests, integration tests, user acceptance testing
- **Code reviews**: Time for reviews and revisions
- **Documentation**: Technical docs, user guides, training materials
- **Deployment**: Deployment planning, execution, rollback preparation
- **Training**: Creating training materials, delivering training
- **Change management**: Communication, user adoption, support
- **Bug fixes**: Fixing issues found during testing
- **Coordination**: Meetings, status updates, alignment

**Estimation approach**: Add percentage buffer (20-30%) for hidden work, or explicitly estimate each category.

## Estimation by Project Phase

### Discovery Phase

**What it is**: Understanding requirements, constraints, and designing solution.

**Typical duration**: 10-20% of total project time.

**Key activities**: Requirements gathering, stakeholder interviews, architecture design, technical feasibility.

### Design Phase

**What it is**: Detailed design of solution components.

**Typical duration**: 10-15% of total project time.

**Key activities**: Data model design, process design, integration design, security design.

### Development Phase

**What it is**: Building the solution.

**Typical duration**: 40-50% of total project time.

**Key activities**: Configuration, development, unit testing, code reviews.

### Testing Phase

**What it is**: Comprehensive testing of solution.

**Typical duration**: 20-25% of total project time.

**Key activities**: Test planning, test execution, bug fixing, regression testing.

### Deployment Phase

**What it is**: Deploying solution to production.

**Typical duration**: 5-10% of total project time.

**Key activities**: Deployment planning, execution, validation, rollback preparation.

# Implementation Guide

## Prerequisites

- Understanding of project scope and requirements
- Knowledge of team capabilities and velocity
- Experience with similar projects
- Understanding of Salesforce platform capabilities

## High-Level Steps

1. **Understand requirements**: Clarify what's needed, document assumptions
2. **Break down work**: Identify all work components by role and phase
3. **Estimate each component**: Use appropriate estimation technique
4. **Account for dependencies**: What must happen before this can start?
5. **Add buffers**: Account for uncertainty, hidden work, risk
6. **Validate estimate**: Compare to similar past projects, sanity check
7. **Communicate estimate**: Present with assumptions, ranges, and tradeoffs

## Key Configuration Decisions

**Estimation granularity**: How detailed should estimates be? More detail = more accuracy but more time to create.

**Buffer percentage**: How much buffer for uncertainty? Depends on project complexity and team experience (typically 20-30%).

**Estimation technique**: Which technique to use? Depends on project phase, requirements clarity, and team practices.

# Common Pitfalls & Anti-Patterns

## Bad Pattern: Optimistic Estimation

**Why it's bad**: Estimates that are too optimistic lead to missed deadlines, disappointed stakeholders, and team burnout.

**Better approach**: Estimate realistically, include buffers, estimate to median talent. It's better to under-promise and over-deliver.

## Bad Pattern: Estimating Only Development Time

**Why it's bad**: Misses significant portions of work (testing, deployment, training, documentation), leading to unrealistic timelines.

**Better approach**: Estimate all phases and roles. Include testing, deployment, training, documentation, and coordination.

## Bad Pattern: Not Accounting for Dependencies

**Why it's bad**: Work can't start until dependencies are complete, but estimates assume immediate start, leading to delays.

**Better approach**: Identify dependencies, estimate dependency completion, include in timeline. Use dependency mapping.

## Bad Pattern: Estimating to Your Own Skill Level

**Why it's bad**: You may be expert, but team members aren't. Estimates based on your skills are unrealistic for team.

**Better approach**: Estimate to median team talent. Account for learning curves and code review time.

# Real-World Scenarios

## Scenario 1: Stakeholder Requests "Simple" Feature

**Problem**: Stakeholder says "It's just adding a field" and expects it done in hours.

**Context**: Feature requires field creation, page layout updates, validation rules, automation, testing, deployment, training.

**Solution**:
- Break down all work components (not just field creation)
- Show time for each component (field: 15 min, layout: 30 min, validation: 1 hour, testing: 2 hours, deployment: 1 hour, training: 1 hour)
- Total: ~6 hours, not 15 minutes
- Explain why each component is necessary
- Get stakeholder buy-in on realistic timeline

## Scenario 2: Estimating Custom Integration

**Problem**: Need to estimate integration with external system, but requirements are unclear.

**Context**: Integration requirements are vague, external system capabilities unknown, authentication approach unclear.

**Solution**:
- Estimate discovery phase first (understand requirements, test integration, design approach)
- Provide range for implementation (best case, worst case, most likely)
- Document assumptions explicitly
- Include time for error handling, testing, and troubleshooting
- Present estimate with confidence level and assumptions

## Scenario 3: Estimating Large Project with Multiple Teams

**Problem**: Need to estimate project involving multiple teams, but coordination overhead is unclear.

**Context**: Project requires Salesforce team, external system team, testing team, and business users.

**Solution**:
- Estimate each team's work separately
- Add coordination overhead (meetings, alignment, integration testing)
- Account for dependencies between teams
- Include buffer for misalignment and rework
- Use phased approach with checkpoints

# Checklist / Mental Model

## Before Estimating

- [ ] Understand requirements (clarify if unclear)
- [ ] Identify all work components (not just development)
- [ ] Identify all roles involved
- [ ] Identify dependencies
- [ ] Understand team capabilities

## During Estimation

- [ ] Break down work into estimable pieces
- [ ] Estimate to median talent, not expert skill
- [ ] Estimate all phases (design, development, testing, deployment)
- [ ] Account for hidden work (reviews, documentation, coordination)
- [ ] Include buffers for uncertainty

## After Estimation

- [ ] Validate estimate (compare to similar projects)
- [ ] Document assumptions explicitly
- [ ] Present estimate with ranges and confidence levels
- [ ] Communicate tradeoffs and options
- [ ] Update estimate as requirements clarify

## Mental Model: Estimation as Communication Tool

Think of estimation as a communication tool, not just a prediction. Good estimates:
- Help stakeholders make informed decisions
- Set realistic expectations
- Enable resource planning
- Support tradeoff discussions
- Build trust through accuracy

# Key Terms & Definitions

- **Effort estimation**: Prediction of work required (person-hours, story points)
- **Time estimation**: Prediction of calendar time required
- **Bottom-up estimation**: Estimating small tasks and summing
- **Top-down estimation**: Estimating overall based on similar projects
- **Three-point estimation**: Using optimistic, pessimistic, and most likely estimates
- **Story points**: Relative sizing using points rather than hours
- **Velocity**: Team's rate of completing work (story points per sprint)
- **Buffer**: Extra time added to account for uncertainty
- **Dependency**: Work that must complete before other work can start

# RAG-Friendly Q&A Seeds

**Q: How do I estimate work when requirements are unclear?**

**A**: Don't estimate unclear requirements. First clarify requirements through questions and stakeholder discussions. Then estimate discovery phase to understand requirements, followed by implementation estimate with documented assumptions. Provide ranges rather than single-point estimates when uncertain.

**Q: Should I estimate to my own skill level or team's average skill level?**

**A**: Estimate to median team talent, not your own expert skill level. You may complete work quickly, but typical team members may take longer. Account for learning curves, code review time, and average team capability in estimates.

**Q: How do I account for all the hidden work in estimates?**

**A**: Either add percentage buffer (20-30%) for hidden work, or explicitly estimate each category: requirements clarification, design, testing, code reviews, documentation, deployment, training, change management, bug fixes, and coordination. Breaking down explicitly is more accurate but time-consuming.

**Q: What's the difference between effort estimation and time estimation?**

**A**: Effort estimation predicts work required (person-hours), while time estimation predicts calendar time. Time depends on effort, number of resources, dependencies, and parallel work. One person working 40 hours = 1 week, but 4 people working 10 hours each = 1 day.

**Q: How do I estimate the lowest-cost OOTB option first?**

**A**: Estimate simplest solution using standard Salesforce features first (baseline cost). Then show cost of each enhancement option (declarative customization, custom development). This helps stakeholders understand baseline before deciding on enhancements and make informed tradeoff decisions.

**Q: What roles should I account for in project estimates?**

**A**: Account for all roles: architects (design, decisions), developers (code), administrators (configuration), business analysts (requirements), testers (testing), project managers (coordination), trainers (training), and documentation (docs). Each role contributes to timeline and must be included.

**Q: How do I guard against unrealistic stakeholder expectations?**

**A**: Break down all work components (not just visible ones), explain dependencies, provide ranges when uncertain, estimate to median talent, include all phases, and account for unknowns. Show stakeholders the full picture, not just the tip of the iceberg.

**Q: What estimation technique should I use?**

**A**: Depends on project phase and requirements clarity. Use bottom-up for well-understood work, top-down for early planning, three-point for high uncertainty, and story points for agile teams with established velocity. Match technique to situation.

**Q: How much buffer should I include in estimates?**

**A**: Typically 20-30% buffer for uncertainty, depending on project complexity and team experience. More complex projects or less experienced teams need larger buffers. Document buffer rationale and assumptions.

**Q: How do I estimate work with broken or scattered requirements?**

**A**: Clarify requirements first through questions and stakeholder discussions. Document assumptions explicitly. Provide wider ranges when requirements are uncertain. Consider phased approach: estimate discovery phase first, then implementation. Include time for requirement clarification and changes in estimate.

## Related Patterns

**See Also**:
- [Stakeholder Communication](/rag/architecture/stakeholder-communication.html) - Communicating with stakeholders
- [Team Leadership](/rag/architecture/team-leadership.html) - Leading development teams

**Related Domains**:
- [Delivery Framework](/rag/project-methods/delivery-framework.html) - Sprint-based delivery approach
- [Testing Strategy](/rag/project-methods/testing-strategy.html) - Testing time estimation

