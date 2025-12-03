---
title: "Building, Leading, and Training Salesforce Development Teams"
source: "The Salesforce Master Class wiki"
source_url: "https://github.com/Coding-With-The-Force/The-Salesforce-Master-Class/wiki"
topic: "Topic 4: The Complete Guide To Salesforce Architecture"
section: "How to Effectively Build, Lead and Train a Team of Devs"
level: "Advanced"
tags:
  - salesforce
  - architecture
  - team-leadership
  - management
  - best-practices
last_reviewed: "2025-01-XX"
---

# Overview

Effective team leadership is essential for successful Salesforce implementations. Architects must build capable teams, lead through influence rather than authority, train team members effectively, and create environments where developers can succeed. Leadership in technical contexts requires balancing technical expertise with people management skills.

Team leadership encompasses finding the right developers, establishing clear expectations, providing guidance and support, facilitating learning, and removing obstacles. Effective leaders serve their teams rather than command them, focusing on enabling success rather than controlling outcomes.

The role of a technical leader is to create conditions where team members can do their best work: clear direction, appropriate resources, learning opportunities, and support when needed. Leadership is about empowerment, not micromanagement.

# Core Concepts

## Finding the Right Developers

**What it is**: Identifying and recruiting developers with the right skills, mindset, and cultural fit for your team.

**Key considerations**:
- **Technical skills**: Apex, LWC, Flow, integration experience
- **Problem-solving ability**: Can they think through complex problems?
- **Learning mindset**: Are they willing to learn and adapt?
- **Communication skills**: Can they work with stakeholders and team members?
- **Cultural fit**: Do they align with team values and working style?

**Hiring strategies**:
- Look for potential, not just current skills (Salesforce skills can be taught)
- Assess problem-solving through technical interviews or coding challenges
- Evaluate communication through behavioral interviews
- Consider diverse backgrounds and perspectives
- Check references for work style and collaboration

**Red flags**:
- Developers who won't follow patterns or best practices
- Developers who can't explain their thinking
- Developers who don't ask questions
- Developers who blame others for problems

## Leading Through Service

**What it is**: The philosophy that leaders serve their teams, not the other way around. Leadership is about enabling success, not exercising authority.

**Service leadership principles**:
- **Remove obstacles**: Identify and eliminate barriers to productivity
- **Provide resources**: Ensure team has tools, access, and information needed
- **Clarify direction**: Provide clear goals and expectations
- **Support growth**: Create learning opportunities and career development
- **Protect the team**: Shield team from unnecessary distractions and politics
- **Celebrate success**: Recognize achievements and contributions

**What service leadership is NOT**:
- Micromanagement or controlling every detail
- Being a pushover or saying yes to everything
- Avoiding difficult conversations
- Taking credit for team work

**Service leadership behaviors**:
- Ask "How can I help?" regularly
- Listen to team concerns and address them
- Make decisions that enable team success
- Share credit, take responsibility for failures
- Invest in team development

## Training and Development

**What it is**: Creating learning opportunities that help developers grow their skills and capabilities.

**Training approaches**:
- **Onboarding**: Structured introduction to org, patterns, and processes
- **Pair programming**: Junior developers work with senior developers
- **Code reviews**: Learning through feedback on actual work
- **Technical sessions**: Team shares knowledge and patterns
- **External training**: Certifications, courses, conferences
- **Stretch assignments**: Challenging work that promotes growth

**Effective training characteristics**:
- **Practical**: Learn by doing, not just reading
- **Relevant**: Training applies to actual work
- **Progressive**: Build skills incrementally
- **Supported**: Help available when stuck
- **Reinforced**: Practice and repetition

**Training anti-patterns**:
- Throwing developers into the deep end without support
- Training that doesn't apply to actual work
- One-time training with no follow-up
- Training without practice opportunities

## Creating a Learning Culture

**What it is**: Environment where learning, experimentation, and growth are encouraged and supported.

**Learning culture elements**:
- **Psychological safety**: Team members feel safe to ask questions and make mistakes
- **Knowledge sharing**: Team members share what they learn
- **Experimentation**: Trying new approaches is encouraged
- **Failure as learning**: Mistakes are learning opportunities, not blame opportunities
- **Continuous improvement**: Regular reflection on what's working and what's not

**How to foster learning culture**:
- Model learning behavior (admit when you don't know, ask questions)
- Celebrate learning, not just success
- Create time for learning (20% time, learning sessions)
- Share failures and what you learned
- Encourage questions and curiosity

# Deep-Dive Patterns & Best Practices

## Team Structure Patterns

### Small Team (2-5 developers)

**Structure**: Flat structure, everyone does everything, direct communication.

**Leadership approach**: Hands-on, involved in day-to-day work, direct feedback.

**Best for**: Small projects, startups, focused initiatives.

### Medium Team (6-15 developers)

**Structure**: May have tech leads or senior developers, some specialization.

**Leadership approach**: More delegation, focus on coordination and alignment.

**Best for**: Medium projects, multiple workstreams, growing organizations.

### Large Team (15+ developers)

**Structure**: Hierarchical with team leads, clear specialization, defined processes.

**Leadership approach**: Strategic focus, process definition, team lead management.

**Best for**: Large projects, enterprise implementations, multiple teams.

## Communication Patterns

### Daily Standups

**Purpose**: Quick alignment, identify blockers, share progress.

**Format**: What did you do yesterday? What will you do today? Any blockers?

**Best practices**: Keep it short (15 minutes), focus on blockers, don't solve problems in standup.

### Code Reviews

**Purpose**: Ensure quality, share knowledge, catch issues early.

**Best practices**: 
- Review for patterns and best practices, not just correctness
- Provide constructive feedback
- Explain why, not just what
- Approve quickly for good code
- Use as teaching opportunity

### Retrospectives

**Purpose**: Reflect on what's working, what's not, and how to improve.

**Format**: What went well? What didn't? What should we change?

**Best practices**: Focus on process, not people. Create action items. Follow up on action items.

## Performance Management

### Setting Expectations

**Clear goals**: Specific, measurable, achievable, relevant, time-bound (SMART).

**Regular feedback**: Don't wait for annual reviews. Provide feedback regularly.

**Growth plans**: Help team members understand career paths and development opportunities.

### Providing Feedback

**Timely**: Provide feedback soon after observation, not months later.

**Specific**: "Your code doesn't follow our patterns" not "Your code is bad."

**Actionable**: Provide guidance on how to improve.

**Balanced**: Include positive feedback, not just areas for improvement.

### Handling Performance Issues

**Early intervention**: Address issues early, don't let them fester.

**Clear communication**: Be direct about expectations and consequences.

**Support**: Provide resources and help for improvement.

**Documentation**: Document conversations and action plans.

# Implementation Guide

## Prerequisites

- Understanding of team dynamics and leadership principles
- Technical expertise to guide and mentor developers
- Communication and interpersonal skills
- Ability to balance technical and people management

## High-Level Steps

1. **Define team structure**: Determine team size, roles, and reporting structure
2. **Establish patterns and standards**: Define coding patterns, best practices, and processes
3. **Create onboarding process**: Structured introduction for new team members
4. **Set up communication channels**: Standups, code reviews, retrospectives
5. **Define growth paths**: Career development and learning opportunities
6. **Establish feedback loops**: Regular one-on-ones, performance reviews
7. **Create learning culture**: Knowledge sharing, experimentation, continuous improvement

## Key Configuration Decisions

**Team size**: Balance between too small (limited capacity) and too large (coordination overhead). Optimal size depends on project complexity and team maturity.

**Specialization vs. generalization**: Should developers specialize (Apex, LWC, integrations) or be generalists? Depends on team size and project needs.

**Reporting structure**: Flat (everyone reports to architect) vs. hierarchical (team leads report to architect). Depends on team size and complexity.

# Common Pitfalls & Anti-Patterns

## Bad Pattern: Micromanagement

**Why it's bad**: Kills autonomy, demotivates team, creates bottlenecks, prevents growth.

**Better approach**: Provide clear direction and expectations, then trust team to execute. Check in regularly but don't control every detail.

## Bad Pattern: Avoiding Difficult Conversations

**Why it's bad**: Performance issues don't resolve themselves. They get worse and damage team culture.

**Better approach**: Address issues directly and early. Have difficult conversations with empathy and clarity.

## Bad Pattern: Not Investing in Team Development

**Why it's bad**: Team skills stagnate, can't take on new challenges, team members leave for growth opportunities.

**Better approach**: Create learning opportunities, provide training, support career development, invest in team growth.

## Bad Pattern: Taking Credit for Team Work

**Why it's bad**: Demotivates team, damages trust, creates resentment.

**Better approach**: Share credit widely, recognize individual contributions, take responsibility for failures.

# Real-World Scenarios

## Scenario 1: Junior Developer Struggling with Complex Patterns

**Problem**: Junior developer consistently produces code that doesn't follow team patterns.

**Context**: Developer is eager and willing to learn but lacks experience with enterprise patterns.

**Solution**:
- Pair program with senior developer
- Provide specific examples of patterns
- Review code together and explain why patterns matter
- Create learning plan with incremental challenges
- Provide positive reinforcement for improvements

## Scenario 2: Senior Developer Resistant to New Patterns

**Problem**: Experienced developer insists on old patterns despite team adopting new approaches.

**Context**: Developer has years of experience but struggles to adapt to new best practices.

**Solution**:
- Understand their concerns (why are they resistant?)
- Explain rationale for new patterns (business value, not just "new")
- Involve them in pattern definition (ownership increases buy-in)
- Provide training and support for transition
- Set clear expectations about adoption timeline

## Scenario 3: Team Member Not Meeting Expectations

**Problem**: Developer consistently misses deadlines or produces low-quality work.

**Context**: Developer has capability but isn't performing to expectations.

**Solution**:
- Have direct conversation about expectations and performance
- Understand root cause (skill gap, motivation, external factors?)
- Create improvement plan with specific goals and timeline
- Provide support and resources for improvement
- Set clear consequences if improvement doesn't occur
- Document conversations and action plans

# Checklist / Mental Model

## Building a Team

- [ ] Define team structure and roles
- [ ] Establish hiring criteria and process
- [ ] Create onboarding process
- [ ] Define patterns and standards
- [ ] Set up communication channels

## Leading a Team

- [ ] Provide clear direction and expectations
- [ ] Remove obstacles and provide resources
- [ ] Facilitate regular communication (standups, one-on-ones)
- [ ] Provide timely feedback
- [ ] Support team member growth

## Training a Team

- [ ] Create learning opportunities (pairing, code reviews, training)
- [ ] Foster learning culture (psychological safety, knowledge sharing)
- [ ] Provide career development guidance
- [ ] Celebrate learning and growth
- [ ] Continuously improve training approaches

## Mental Model: Leader as Enabler

Think of yourself as an enabler, not a controller. Your job is to:
- Create conditions where team can succeed
- Remove obstacles and provide resources
- Guide and support, not command and control
- Serve the team, not be served by the team

# Key Terms & Definitions

- **Service leadership**: Leadership philosophy focused on serving and enabling team success
- **Pair programming**: Two developers work together on same code, one writes, one reviews
- **Code review**: Process of reviewing code for quality, patterns, and knowledge sharing
- **Retrospective**: Regular meeting to reflect on what's working and what to improve
- **Psychological safety**: Environment where team members feel safe to take risks and make mistakes
- **Onboarding**: Structured process for introducing new team members
- **Mentoring**: Relationship where experienced developer guides less experienced developer

# RAG-Friendly Q&A Seeds

**Q: How do I find the right developers for my Salesforce team?**

**A**: Look for problem-solving ability, learning mindset, and communication skills, not just current Salesforce knowledge. Assess through technical interviews, coding challenges, and behavioral interviews. Consider diverse backgrounds and check references for work style.

**Q: What's the difference between managing and leading a development team?**

**A**: Management is about planning, organizing, and controlling. Leadership is about inspiring, enabling, and serving. Effective technical leaders focus on enabling success (removing obstacles, providing resources, supporting growth) rather than controlling outcomes.

**Q: How do I train junior developers effectively?**

**A**: Use practical, relevant training that applies to actual work. Pair program with senior developers, use code reviews as teaching opportunities, provide progressive challenges, and create psychological safety for asking questions. Reinforce learning through practice and repetition.

**Q: How do I handle a developer who isn't meeting expectations?**

**A**: Have direct conversation about expectations and performance. Understand root cause (skill gap, motivation, external factors). Create improvement plan with specific goals and timeline. Provide support and resources. Set clear consequences if improvement doesn't occur. Document conversations.

**Q: What's the best way to provide feedback to developers?**

**A**: Provide feedback timely (soon after observation), specifically ("Your code doesn't follow our patterns" not "Your code is bad"), and actionably (guidance on how to improve). Balance positive feedback with areas for improvement. Use code reviews as teaching opportunities.

**Q: How do I create a learning culture on my team?**

**A**: Model learning behavior (admit when you don't know, ask questions), celebrate learning not just success, create time for learning, share failures and what you learned, and encourage questions and curiosity. Create psychological safety where team members feel safe to experiment and make mistakes.

**Q: Should developers specialize or be generalists?**

**A**: Depends on team size and project needs. Small teams benefit from generalists who can work across areas. Large teams can support specialization. Consider project complexity, team capacity, and career development goals when deciding.

**Q: How do I prevent micromanagement while ensuring quality?**

**A**: Provide clear direction and expectations, establish patterns and standards, use code reviews for quality, trust team to execute, and check in regularly without controlling every detail. Focus on outcomes and results, not process and methods.

**Q: What's the best team structure for Salesforce development?**

**A**: Depends on team size. Small teams (2-5) use flat structure with direct communication. Medium teams (6-15) may have tech leads and some specialization. Large teams (15+) need hierarchical structure with team leads and defined processes.

**Q: How do I balance being a technical leader and people manager?**

**A**: Maintain technical expertise to guide and mentor, but focus leadership on enabling success rather than doing all technical work yourself. Delegate technical work to team, focus your time on removing obstacles, providing resources, and supporting growth. Balance hands-on technical work with leadership responsibilities.

## Related Patterns

**See Also**:
- [Architect Role](architecture/architect-role.html) - Architect leadership responsibilities
- [Stakeholder Communication](architecture/stakeholder-communication.html) - Communication patterns
- [Project Estimation](architecture/project-estimation.html) - Team estimation patterns

**Related Domains**:
- [Governance Patterns](architecture/governance-patterns.html) - Team governance and standards
- [Delivery Framework](project-methods/delivery-framework.html) - Team coordination in sprints

