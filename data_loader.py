"""
Data loader module for adding substantial data to the RAG system.
"""
from rag_engine import RAGEngine

def load_gc_forms_data(rag_engine):
    """
    Load more comprehensive GC Forms documentation into the RAG system.
    
    Args:
        rag_engine: The RAG engine to load data into
    
    Returns:
        int: Number of documents added
    """
    print("Loading comprehensive GC Forms documentation...")
    docs_added = 0
    
    # GC Forms Overview
    overview = """
    GC Forms is a powerful form creation and management system built for enterprise use.
    The platform allows organizations to create, distribute, and analyze forms and surveys
    with advanced features for data collection and analysis.
    
    GC Forms provides a secure environment for gathering sensitive information,
    with compliance features that meet stringent regulatory requirements. Users can
    create forms from scratch or use templates, customize them with branding,
    and deploy them to targeted audiences.
    
    The platform integrates seamlessly with other enterprise systems, allowing for
    automated workflows and data synchronization across the organization.
    """
    
    rag_engine.add_document(overview, {
        "type": "overview",
        "title": "GC Forms Platform Overview",
        "section": "introduction"
    })
    docs_added += 1
    
    # Form Creation Features
    form_creation = """
    # Form Creation Features in GC Forms
    
    GC Forms offers an intuitive drag-and-drop interface for building forms of any complexity.
    
    ## Question Types
    - Short Text: For names, brief answers, and simple inputs
    - Long Text: For detailed responses and comments
    - Multiple Choice: Radio buttons for selecting a single option
    - Checkboxes: For selecting multiple options
    - Dropdown Menus: Space-efficient selection for many options
    - Date and Time: For scheduling and time-based data
    - File Upload: Allow users to attach documents, images, etc.
    - Rating Scales: Linear scales, star ratings, numerical ratings
    - Matrix Questions: Grid layout for multiple related questions
    - Ranking: For ordering preferences
    
    ## Form Logic
    - Conditional Logic: Show or hide questions based on previous answers
    - Branch Logic: Create different paths through the form
    - Skip Logic: Skip irrelevant sections based on responses
    - Calculation Fields: Perform math operations on form data
    - Input Validation: Ensure data quality and format compliance
    
    ## Design Features
    - Custom Themes: Apply branding with colors, fonts, and logos
    - Page Breaks: Organize questions across multiple pages
    - Progress Indicators: Show completion percentage
    - Custom CSS: Advanced styling for unique requirements
    - Mobile Optimization: Responsive design for all devices
    """
    
    rag_engine.add_document(form_creation, {
        "type": "feature",
        "title": "Form Creation Features",
        "section": "features"
    })
    docs_added += 1
    
    # Distribution & Collection
    distribution = """
    # Distribution and Collection in GC Forms
    
    GC Forms offers flexible options for distributing forms and collecting responses.
    
    ## Distribution Methods
    - Direct Links: Share simple URLs to your forms
    - Email Campaigns: Send forms directly to recipient lists
    - Embed Options: Add forms to websites or internal portals
    - QR Codes: Generate scannable codes for physical distribution
    - API Integration: Programmatically create and distribute forms
    
    ## Response Collection
    - Real-time Data: See responses as they come in
    - Response Limits: Set maximum number of submissions
    - Scheduling: Open and close forms automatically
    - Authentication: Require login or verification before submission
    - Save and Resume: Allow users to save progress and continue later
    
    ## Notification Systems
    - Email Alerts: Get notified of new submissions
    - Automated Responses: Send confirmation emails to respondents
    - Team Notifications: Alert relevant stakeholders based on responses
    - Threshold Alerts: Get notified when response rates reach certain levels
    """
    
    rag_engine.add_document(distribution, {
        "type": "feature",
        "title": "Distribution and Collection",
        "section": "features"
    })
    docs_added += 1
    
    # Data Analysis
    analysis = """
    # Data Analysis in GC Forms
    
    GC Forms provides robust tools for analyzing form responses and extracting insights.
    
    ## Reporting Tools
    - Summary Reports: Get an overview of all responses
    - Individual Views: Examine specific submissions in detail
    - Filter and Segment: Analyze subsets of your data
    - Cross-Tabulation: Compare answers between different questions
    - Trend Analysis: Track changes in responses over time
    
    ## Visualization Options
    - Charts and Graphs: Bar, pie, line charts for quantitative data
    - Word Clouds: Visualize common terms in text responses
    - Heat Maps: Identify patterns in matrix questions
    - Geographic Maps: Visualize location-based data
    - Custom Dashboards: Create personalized data views
    
    ## Export and Integration
    - Multiple Formats: Export to CSV, Excel, PDF, etc.
    - API Access: Pull analytics data programmatically
    - BI Integration: Connect to business intelligence platforms
    - Scheduled Reports: Automatically generate and send reports
    - Raw Data Access: Download complete datasets for custom analysis
    """
    
    rag_engine.add_document(analysis, {
        "type": "feature",
        "title": "Data Analysis Features",
        "section": "features"
    })
    docs_added += 1
    
    # Security Features
    security = """
    # Security and Compliance in GC Forms
    
    GC Forms takes security and regulatory compliance seriously with comprehensive measures.
    
    ## Data Protection
    - End-to-End Encryption: Secure data in transit and at rest
    - Access Controls: Granular permissions for users and groups
    - Audit Trails: Track all system activities and changes
    - Data Residency: Control where your data is stored
    - Backup and Recovery: Automated data protection measures
    
    ## Compliance Features
    - GDPR Tools: Data subject access requests, right to be forgotten
    - HIPAA Compliance: Features for handling protected health information
    - Accessibility: WCAG 2.1 AA compliance for inclusive forms
    - Custom Retention: Set data retention policies
    - PII Protection: Tools for handling personally identifiable information
    
    ## Authentication Options
    - Single Sign-On: Integrate with enterprise identity providers
    - Multi-factor Authentication: Additional security layers
    - IP Restrictions: Limit form access by location
    - Email Verification: Confirm respondent identities
    - Custom Authentication: Build your own verification processes
    """
    
    rag_engine.add_document(security, {
        "type": "feature",
        "title": "Security and Compliance",
        "section": "security"
    })
    docs_added += 1
    
    # API Documentation
    api_docs = """
    # GC Forms API Documentation
    
    The GC Forms API allows developers to programmatically create, manage, and analyze forms.
    
    ## Authentication
    All API requests require authentication using OAuth 2.0 bearer tokens:
    
    ```
    Authorization: Bearer YOUR_API_TOKEN
    ```
    
    ## Form Management Endpoints
    
    ### GET /api/v1/forms
    List all forms accessible to the authenticated user.
    
    Parameters:
    - page: Page number for pagination (default: 1)
    - limit: Items per page (default: 20)
    - status: Filter by form status (draft, active, closed)
    
    ### POST /api/v1/forms
    Create a new form.
    
    Request body:
    ```json
    {
      "title": "Form Title",
      "description": "Form description",
      "questions": [
        {
          "type": "text",
          "title": "Question text",
          "required": true
        }
      ]
    }
    ```
    
    ### GET /api/v1/forms/{formId}
    Retrieve a specific form by ID.
    
    ### PUT /api/v1/forms/{formId}
    Update an existing form.
    
    ### DELETE /api/v1/forms/{formId}
    Delete a form.
    
    ## Response Management
    
    ### GET /api/v1/forms/{formId}/responses
    List all responses for a specific form.
    
    ### POST /api/v1/forms/{formId}/responses
    Submit a new response to a form.
    
    ### GET /api/v1/forms/{formId}/responses/{responseId}
    Retrieve a specific response.
    
    ## Analytics
    
    ### GET /api/v1/forms/{formId}/analytics
    Get analytics data for a specific form.
    
    Parameters:
    - from: Start date (ISO format)
    - to: End date (ISO format)
    - metrics: Comma-separated list of metrics
    """
    
    rag_engine.add_document(api_docs, {
        "type": "technical",
        "title": "API Documentation",
        "section": "developers"
    })
    docs_added += 1
    
    print(f"Successfully loaded {docs_added} GC Forms documents")
    return docs_added
