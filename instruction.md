# Development Roadmap Request: Political Fact-Checking Web Application

## Role and Context
You are an expert Python developer and coding mentor specializing in full-stack web development and project architecture. I need a comprehensive development roadmap for building a web application from scratch.

## Project Overview
**Application Name**: The Sauce Bottle  
**Purpose**: Track Australian politicians' statement accuracy by:
- Scraping news websites for political statements
- Cross-referencing against historical statements to identify contradictions
- Providing fact-checking capabilities
- Offering ethical monetization options

**Key Constraints**: 
- Must be implementable cheaply for initial deployment
- Designed for a time-poor developer working in small increments
- Should support learning progression from intermediate to advanced skills

## Technical Stack Requirements
- **Dependency Management**: pixi
- **Frontend**: Vue.js
- **Backend**: Python with FastAPI
- **Database**: PostgreSQL with SQLAlchemy ORM and Flyway migrations
- **Containerization**: Docker
- **Deployment**: AWS (cost-effective services)
- **Version Control**: Git with CI/CD workflows

## Developer Background
- **Python**: Comfortable/intermediate level
- **Web Development**: Minimal experience
- **HTML/CSS**: Basic competency
- **JavaScript**: Rusty, needs refresher
- **Database**: Some experience implied
- **DevOps**: Limited (needs guidance on Docker, CI/CD, AWS)

## Required Deliverables
Create a detailed development roadmap that includes:

1. **Learning-Oriented Structure**
   - Progressive skill-building milestones
   - Specific technologies to master at each phase
   - Recommended learning resources for each component

2. **Incremental Development Plan**
   - Logical, chronological phases
   - Time estimates for each phase (assuming 5-10 hours per week)
   - Clear deliverables and success criteria for each increment

3. **Technical Architecture**
   - System design recommendations
   - Database schema considerations
   - API structure planning
   - Deployment architecture

4. **Implementation Strategy**
   - Step-by-step setup instructions for development environment
   - Best practices for the chosen tech stack
   - Testing strategies for each component
   - Cost optimization strategies for AWS deployment

## Specific Questions to Address
Before providing the roadmap, please clarify:

1. **Scope Prioritization**: What's the minimum viable product (MVP) you'd want to launch first?

2. **Data Sources**: Do you have specific Australian news sites in mind for scraping, and are you aware of their terms of service?

3. **Legal Considerations**: Have you considered the legal implications of automated fact-checking and politician tracking?

4. **Monetization Timeline**: When do you plan to implement monetization features relative to core functionality?

5. **Scalability Requirements**: What's your expected user base in year one vs. long-term?

6. **Content Moderation**: How do you plan to handle accuracy verification and potential disputes about fact-checking results?
