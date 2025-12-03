---
title: "Stakeholder Communication for Salesforce Architects"
source: "The Salesforce Master Class wiki"
source_url: "https://github.com/Coding-With-The-Force/The-Salesforce-Master-Class/wiki"
topic: "Topic 4: The Complete Guide To Salesforce Architecture"
section: "The Basics of Communication"
level: "Intermediate"
tags:
  - salesforce
  - architecture
  - communication
  - stakeholder-management
  - best-practices
last_reviewed: "2025-01-XX"
---

# Overview

Effective communication is fundamental to successful Salesforce architecture. Architects must translate complex technical concepts into business language, manage stakeholder expectations, build trust, and facilitate decision-making. Communication skills often determine project success more than technical expertise alone.

Stakeholder communication encompasses understanding different audiences (executives, business users, developers, project managers), adapting communication style and detail level, asking the right questions to uncover requirements, setting realistic expectations, and establishing credibility through consistent delivery.

Architects serve as bridges between business needs and technical solutions, requiring the ability to listen actively, ask clarifying questions, present options clearly, and guide stakeholders toward informed decisions. Effective communication prevents scope creep, manages expectations, and builds organizational trust in the architecture function.

# Core Concepts

## Understanding Stakeholder Audiences

**What it is**: Different stakeholder groups have different needs, technical understanding, and communication preferences.

**Key stakeholder types**:
- **Executives**: Need high-level business impact, ROI, risk assessment, strategic alignment
- **Business users**: Need process understanding, user experience, training, support
- **Project managers**: Need timelines, dependencies, risks, resource requirements
- **Developers**: Need technical specifications, constraints, patterns, implementation details
- **Security/compliance**: Need security controls, data protection, audit trails, compliance requirements

**Communication approach**:
- Adapt detail level to audience (high-level for executives, detailed for developers)
- Use appropriate language (business terms for business stakeholders, technical terms for technical stakeholders)
- Focus on what matters to each audience (business value for executives, implementation details for developers)
- Provide context and rationale for decisions

## Asking Effective Questions

**What it is**: The ability to ask questions that uncover real requirements, constraints, and priorities rather than surface-level wants.

**Question types**:
- **Open-ended questions**: "What problem are you trying to solve?" rather than "Do you want feature X?"
- **Context questions**: "What happens today?" to understand current state
- **Constraint questions**: "What are the limitations we need to work within?" (budget, timeline, resources)
- **Priority questions**: "If we can only do one thing, what would it be?" to understand priorities
- **Success criteria questions**: "How will you know this is successful?" to define success

**Best practices**:
- Ask "why" to understand root causes, not just symptoms
- Ask about edge cases and exceptions, not just happy paths
- Ask about integration points and dependencies
- Ask about future needs and scalability requirements
- Listen more than you speak

## Setting Realistic Expectations

**What it is**: Clearly communicating what is possible, what is not, timelines, costs, and tradeoffs so stakeholders make informed decisions.

**Key elements**:
- **Scope boundaries**: What's included, what's excluded, what's out of scope
- **Timeline reality**: Realistic estimates based on complexity, not wishful thinking
- **Cost transparency**: Total cost of ownership, not just initial implementation
- **Tradeoff communication**: "If we do X, we can't do Y" or "X is faster but Y is more flexible"
- **Risk communication**: Known risks, mitigation strategies, contingency plans

**Best practices**:
- Estimate to median talent, not your own skills
- Estimate lowest-cost OOTB option first, not ideal end result
- Include all phases (design, development, testing, deployment, training)
- Communicate dependencies and assumptions
- Provide ranges when uncertain, not false precision

## Building Trust with Stakeholders

**What it is**: Establishing credibility and reliability through consistent delivery, honest communication, and demonstrated expertise.

**Trust-building behaviors**:
- **Deliver on commitments**: Meet deadlines, deliver quality, communicate proactively
- **Admit when you don't know**: Say "I need to research that" rather than guessing
- **Be transparent about challenges**: Share problems early, propose solutions
- **Demonstrate expertise**: Show deep understanding of platform capabilities and constraints
- **Listen actively**: Understand stakeholder concerns and incorporate feedback
- **Follow through**: Complete what you start, close loops, provide updates

**Trust indicators**:
- Stakeholders bring you in early on projects
- Stakeholders accept your recommendations
- Stakeholders share concerns and challenges openly
- Stakeholders involve you in strategic decisions

# Deep-Dive Patterns & Best Practices

## Communication Patterns for Different Scenarios

### Initial Requirements Gathering

**Pattern**: Start broad, then narrow down through iterative questioning.

**Approach**:
1. Understand the business problem (not the proposed solution)
2. Understand current state and pain points
3. Understand success criteria and constraints
4. Propose options with tradeoffs
5. Refine based on feedback

**Example**: Instead of "Do you want a custom object?", ask "What information do you need to track? How do you track it today? What problems does that create?"

### Presenting Architecture Options

**Pattern**: Present multiple options with clear tradeoffs, not just one recommendation.

**Structure**:
- **Option 1**: OOTB approach (fastest, lowest cost, least flexible)
- **Option 2**: Declarative customization (moderate speed/cost, good flexibility)
- **Option 3**: Custom development (slowest, highest cost, most flexible)

**For each option, provide**:
- Timeline estimate
- Cost estimate
- Flexibility/limitations
- Maintenance requirements
- Risk assessment

### Managing Scope Creep

**Pattern**: Use structured change management rather than ad-hoc additions.

**Approach**:
- Document original scope clearly
- Require formal change requests for additions
- Assess impact (timeline, cost, risk) for each change
- Get stakeholder approval for changes
- Update documentation and timelines

**Communication**: "That's a great idea. Let me assess the impact on timeline and cost, and we can decide if we add it to this phase or a future phase."

### Communicating Technical Constraints

**Pattern**: Explain constraints in business terms, not just technical terms.

**Approach**:
- Don't say "Salesforce doesn't support that"
- Say "Here's what Salesforce supports, and here's how we can achieve your goal within those capabilities"
- Provide alternatives when constraints exist
- Explain why constraints exist (platform architecture, security, performance)

**Example**: Instead of "You can't do that in Salesforce", say "Salesforce handles that differently. Here are three ways to achieve your goal..."

# Implementation Guide

## Prerequisites

- Understanding of stakeholder roles and needs
- Knowledge of Salesforce platform capabilities and constraints
- Ability to translate between business and technical language
- Active listening skills
- Questioning techniques

## High-Level Steps

1. **Identify stakeholders**: Map all stakeholders, their roles, interests, and influence
2. **Understand communication preferences**: How do they prefer to receive information? (email, meetings, documentation)
3. **Establish communication cadence**: Regular check-ins, status updates, decision points
4. **Create communication templates**: Standard formats for status updates, architecture decisions, change requests
5. **Practice active listening**: Listen to understand, not just to respond
6. **Document decisions**: Capture decisions, rationale, and assumptions
7. **Follow up**: Close loops, provide updates, confirm understanding

## Key Configuration Decisions

**Communication frequency**: How often to communicate depends on project phase and stakeholder needs. Daily during critical phases, weekly during steady-state, ad-hoc for urgent issues.

**Communication channels**: Choose appropriate channels (email for documentation, meetings for discussion, Slack for quick questions).

**Detail level**: Match detail level to audience. Executives need summaries, developers need specifications.

**Documentation level**: Balance between too little (stakeholders don't understand) and too much (stakeholders don't read).

# Common Pitfalls & Anti-Patterns

## Bad Pattern: Technical Jargon with Business Stakeholders

**Why it's bad**: Business stakeholders don't understand technical terms, leading to miscommunication and poor decisions.

**Better approach**: Use business language. Explain technical concepts in terms of business impact. Use analogies when helpful.

## Bad Pattern: Saying Yes to Everything

**Why it's bad**: Leads to scope creep, missed deadlines, and stakeholder disappointment when you can't deliver.

**Better approach**: Assess requests, communicate tradeoffs, get approval for changes. Say "Let me assess the impact" rather than immediately saying yes or no.

## Bad Pattern: Avoiding Difficult Conversations

**Why it's bad**: Problems don't go away when ignored. They get worse and damage trust.

**Better approach**: Share challenges early, propose solutions, involve stakeholders in problem-solving.

## Bad Pattern: Not Listening to Stakeholders

**Why it's bad**: You miss requirements, make wrong assumptions, and build solutions that don't meet needs.

**Better approach**: Listen actively. Ask clarifying questions. Confirm understanding. Incorporate feedback.

# Real-World Scenarios

## Scenario 1: Executive Wants Feature in Unrealistic Timeline

**Problem**: Executive requests complex feature with two-week deadline that realistically needs two months.

**Context**: Feature requires custom development, integration with external system, and testing.

**Solution**: 
- Acknowledge the business need
- Break down what's required (design, development, integration, testing)
- Provide realistic timeline with rationale
- Offer phased approach (MVP in two weeks, full feature in two months)
- Get executive buy-in on approach

## Scenario 2: Business User Requests Feature That Conflicts with Platform Best Practices

**Problem**: Business user wants workflow that conflicts with Salesforce best practices (e.g., 50 record types on one object).

**Context**: User has valid business need but proposed solution creates maintenance and performance issues.

**Solution**:
- Understand the underlying business need
- Explain why the proposed approach creates problems
- Propose alternative approaches that meet the need within best practices
- Show how alternative approaches solve the business problem
- Get user buy-in on better approach

## Scenario 3: Multiple Stakeholders Have Conflicting Requirements

**Problem**: Different stakeholder groups want different solutions for the same requirement.

**Context**: Sales wants one process, Service wants another, and they conflict.

**Solution**:
- Facilitate discussion between stakeholders
- Identify common goals and differences
- Propose solution that meets core needs of both groups
- Use configuration (record types, profiles) to support different processes
- Get consensus on approach

# Checklist / Mental Model

## Before Any Stakeholder Meeting

- [ ] Know your audience (roles, technical level, interests)
- [ ] Prepare key messages and questions
- [ ] Review relevant context (previous decisions, constraints, dependencies)
- [ ] Prepare to listen more than speak

## During Stakeholder Communication

- [ ] Use appropriate language for audience
- [ ] Ask open-ended questions to understand needs
- [ ] Confirm understanding ("So if I understand correctly...")
- [ ] Present options with tradeoffs, not just recommendations
- [ ] Be honest about uncertainties and constraints

## After Stakeholder Communication

- [ ] Document decisions and rationale
- [ ] Follow up on action items
- [ ] Update stakeholders on progress
- [ ] Close loops on questions and concerns

## Mental Model: Architect as Translator

Think of yourself as a translator between business language and technical language. Your job is to:
- Understand business needs in business terms
- Translate to technical solutions
- Translate technical constraints to business impact
- Facilitate informed decision-making

# Key Terms & Definitions

- **Stakeholder**: Any person or group with interest in or influence over the project
- **Requirements gathering**: Process of understanding what stakeholders need
- **Scope creep**: Uncontrolled expansion of project scope
- **Change request**: Formal request to modify project scope, timeline, or budget
- **Expectation management**: Process of setting and maintaining realistic expectations
- **Active listening**: Listening to understand, not just to respond
- **Stakeholder mapping**: Identifying all stakeholders and their roles/interests

# RAG-Friendly Q&A Seeds

**Q: How do I communicate technical constraints to non-technical stakeholders?**

**A**: Explain constraints in business terms. Instead of "Salesforce doesn't support that", say "Here's what Salesforce supports, and here are three ways to achieve your goal within those capabilities." Provide alternatives and explain business impact of constraints.

**Q: How do I handle stakeholders who want everything immediately?**

**A**: Acknowledge their needs, break down what's required, provide realistic timelines with rationale, and offer phased approaches (MVP first, full solution later). Get buy-in on approach rather than just saying no.

**Q: What questions should I ask to understand real requirements?**

**A**: Ask open-ended questions about the problem ("What problem are you trying to solve?"), current state ("What happens today?"), constraints ("What are the limitations?"), priorities ("If we can only do one thing, what would it be?"), and success criteria ("How will you know this is successful?").

**Q: How do I build trust with stakeholders?**

**A**: Deliver on commitments, admit when you don't know something, be transparent about challenges, demonstrate expertise, listen actively, and follow through on promises. Trust is built through consistent behavior over time.

**Q: How do I prevent scope creep?**

**A**: Document original scope clearly, require formal change requests for additions, assess impact (timeline, cost, risk) for each change, get stakeholder approval, and update documentation. Use structured change management rather than ad-hoc additions.

**Q: How do I present architecture options to stakeholders?**

**A**: Present multiple options (OOTB, declarative, custom) with clear tradeoffs. For each option, provide timeline estimate, cost estimate, flexibility/limitations, maintenance requirements, and risk assessment. Let stakeholders make informed decisions.

**Q: What's the best way to communicate with executives?**

**A**: Focus on business impact, ROI, risk assessment, and strategic alignment. Use high-level language, avoid technical jargon, provide summaries not details, and focus on what matters to them (business value, not implementation details).

**Q: How do I handle conflicting requirements from different stakeholders?**

**A**: Facilitate discussion between stakeholders, identify common goals and differences, propose solutions that meet core needs of both groups, use configuration to support different processes, and get consensus on approach.

**Q: What should I do when I don't know the answer to a stakeholder question?**

**A**: Admit you don't know, commit to researching it, provide a timeline for getting back to them, and follow through. Don't guess or make up answers - it damages trust.

**Q: How often should I communicate with stakeholders?**

**A**: Frequency depends on project phase and stakeholder needs. Daily during critical phases, weekly during steady-state, ad-hoc for urgent issues. Match communication cadence to project needs and stakeholder preferences.

## Related Patterns

**See Also**:
- <a href="{{ '/rag/architecture/architecture/architect-role.html' | relative_url }}">Architect Role</a> - Architect communication responsibilities
- <a href="{{ '/rag/architecture/architecture/team-leadership.html' | relative_url }}">Team Leadership</a> - Team communication patterns
- <a href="{{ '/rag/architecture/architecture/project-estimation.html' | relative_url }}">Project Estimation</a> - Managing stakeholder expectations

**Related Domains**:
- <a href="{{ '/rag/architecture/project-methods/delivery-framework.html' | relative_url }}">Delivery Framework</a> - Stakeholder coordination in sprints

