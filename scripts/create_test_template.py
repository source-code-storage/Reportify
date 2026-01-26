"""
Create a test PDF template for the Report Writing Assistant
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY


def create_test_template():
    """Create a comprehensive test template PDF"""

    # Create PDF
    filename = "PFE_Project_Template.pdf"
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=18,
    )

    # Container for the 'Flowable' objects
    elements = []

    # Define styles
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        "CustomTitle",
        parent=styles["Heading1"],
        fontSize=24,
        textColor="darkblue",
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName="Helvetica-Bold",
    )

    heading1_style = ParagraphStyle(
        "CustomHeading1",
        parent=styles["Heading1"],
        fontSize=16,
        textColor="darkblue",
        spaceAfter=12,
        spaceBefore=12,
        fontName="Helvetica-Bold",
    )

    heading2_style = ParagraphStyle(
        "CustomHeading2",
        parent=styles["Heading2"],
        fontSize=14,
        textColor="navy",
        spaceAfter=10,
        spaceBefore=10,
        fontName="Helvetica-Bold",
    )

    normal_style = ParagraphStyle(
        "CustomNormal",
        parent=styles["Normal"],
        fontSize=11,
        alignment=TA_JUSTIFY,
        spaceAfter=12,
    )

    # Cover Page
    elements.append(Spacer(1, 2 * inch))
    elements.append(Paragraph("PFE Project Report Template", title_style))
    elements.append(Spacer(1, 0.5 * inch))
    elements.append(Paragraph("<b>Student Name:</b> [Your Name]", normal_style))
    elements.append(Paragraph("<b>Supervisor:</b> [Supervisor Name]", normal_style))
    elements.append(Paragraph("<b>Institution:</b> [University Name]", normal_style))
    elements.append(Paragraph("<b>Academic Year:</b> 2025-2026", normal_style))
    elements.append(PageBreak())

    # Acknowledgements
    elements.append(Paragraph("Acknowledgements", heading1_style))
    elements.append(
        Paragraph(
            "I would like to express my sincere gratitude to all those who contributed to the "
            "successful completion of this project. Special thanks to my supervisor for their "
            "guidance and support throughout this journey. I am also grateful to my family and "
            "friends for their encouragement and understanding.",
            normal_style,
        )
    )
    elements.append(PageBreak())

    # Abstract
    elements.append(Paragraph("Abstract", heading1_style))
    elements.append(
        Paragraph(
            "This project focuses on developing an innovative solution for [problem domain]. "
            "The main objectives were to design, implement, and evaluate a system that addresses "
            "[specific challenges]. The methodology employed includes requirements analysis, "
            "system design, implementation, and comprehensive testing. The results demonstrate "
            "significant improvements in [key metrics]. This work contributes to the field by "
            "providing [main contribution].",
            normal_style,
        )
    )
    elements.append(PageBreak())

    # Résumé (French)
    elements.append(Paragraph("Résumé", heading1_style))
    elements.append(
        Paragraph(
            "Ce projet se concentre sur le développement d'une solution innovante pour [domaine du problème]. "
            "Les principaux objectifs étaient de concevoir, mettre en œuvre et évaluer un système qui répond "
            "à [défis spécifiques]. La méthodologie employée comprend l'analyse des exigences, la conception "
            "du système, la mise en œuvre et des tests complets. Les résultats démontrent des améliorations "
            "significatives dans [métriques clés]. Ce travail contribue au domaine en fournissant "
            "[contribution principale].",
            normal_style,
        )
    )
    elements.append(PageBreak())

    # Table of Contents
    elements.append(Paragraph("Table of Contents", heading1_style))
    toc_items = [
        "Acknowledgements .................................................... 2",
        "Abstract ............................................................ 3",
        "Résumé (French) ..................................................... 4",
        "Table of Contents ................................................... 5",
        "List of Acronyms .................................................... 6",
        "Introduction ........................................................ 7",
        "Chapter 1: Context and Problem Statement ............................ 8",
        "Chapter 2: Literature Review ........................................ 12",
        "Chapter 3: Methodology and System Design ............................ 16",
        "Chapter 4: Implementation ........................................... 20",
        "Chapter 5: Results and Discussion ................................... 24",
        "Chapter 6: Conclusion and Future Work ............................... 28",
        "General Conclusion .................................................. 30",
        "Bibliography / References ........................................... 31",
        "Appendices .......................................................... 32",
    ]
    for item in toc_items:
        elements.append(Paragraph(item, normal_style))
    elements.append(PageBreak())

    # List of Acronyms
    elements.append(Paragraph("List of Acronyms", heading1_style))
    acronyms = [
        "<b>AI</b> - Artificial Intelligence",
        "<b>API</b> - Application Programming Interface",
        "<b>CRUD</b> - Create, Read, Update, Delete",
        "<b>DB</b> - Database",
        "<b>HTTP</b> - Hypertext Transfer Protocol",
        "<b>JSON</b> - JavaScript Object Notation",
        "<b>ML</b> - Machine Learning",
        "<b>REST</b> - Representational State Transfer",
        "<b>SQL</b> - Structured Query Language",
        "<b>UI</b> - User Interface",
    ]
    for acronym in acronyms:
        elements.append(Paragraph(acronym, normal_style))
    elements.append(PageBreak())

    # Introduction
    elements.append(Paragraph("Introduction", heading1_style))
    elements.append(
        Paragraph(
            "In today's rapidly evolving technological landscape, organizations face increasing "
            "challenges in managing and processing information efficiently. This project addresses "
            "the need for automated solutions that can streamline complex workflows and improve "
            "productivity.",
            normal_style,
        )
    )
    elements.append(Paragraph("The main objectives of this project are:", normal_style))
    objectives = [
        "1. To develop a comprehensive system architecture",
        "2. To implement core functionality using modern technologies",
        "3. To evaluate system performance and usability",
        "4. To demonstrate practical applications and benefits",
    ]
    for obj in objectives:
        elements.append(Paragraph(obj, normal_style))
    elements.append(
        Paragraph(
            "This report is organized as follows: Chapter 1 presents the context and problem statement. "
            "Chapter 2 reviews the relevant literature. Chapter 3 describes the methodology and system "
            "design. Chapter 4 details the implementation. Chapter 5 presents and discusses the results. "
            "Chapter 6 concludes the work and suggests future directions.",
            normal_style,
        )
    )
    elements.append(PageBreak())

    # Chapter 1: Context and Problem Statement
    elements.append(
        Paragraph("Chapter 1: Context and Problem Statement", heading1_style)
    )

    elements.append(Paragraph("1.1 Background", heading2_style))
    elements.append(
        Paragraph(
            "The background of this project lies in the growing need for efficient information "
            "management systems. Recent developments in artificial intelligence and machine learning "
            "have shown promising results in automating complex tasks. This creates an opportunity "
            "to develop innovative solutions that leverage these technologies.",
            normal_style,
        )
    )

    elements.append(Paragraph("1.2 Problem Statement", heading2_style))
    elements.append(
        Paragraph(
            "The main problem addressed in this project is the inefficiency of manual processes in "
            "handling large volumes of data. Current solutions suffer from limited automation, poor "
            "scalability, and lack of intelligent features. There is a need for a comprehensive system "
            "that can automate workflows while maintaining accuracy and reliability.",
            normal_style,
        )
    )
    elements.append(Paragraph("Specifically, the challenges include:", normal_style))
    challenges = [
        "• Time-consuming manual data entry and processing",
        "• Difficulty in extracting relevant information from documents",
        "• Lack of intelligent search and retrieval capabilities",
        "• Limited integration with existing systems",
    ]
    for challenge in challenges:
        elements.append(Paragraph(challenge, normal_style))

    elements.append(Paragraph("1.3 Objectives", heading2_style))
    elements.append(
        Paragraph(
            "The primary objective of this project is to design and implement an intelligent system "
            "that addresses the identified challenges. The specific objectives are:",
            normal_style,
        )
    )
    specific_objectives = [
        "1. <b>Objective 1:</b> Design a scalable system architecture that supports future extensions",
        "2. <b>Objective 2:</b> Implement automated document processing capabilities",
        "3. <b>Objective 3:</b> Integrate AI-powered features for intelligent content generation",
        "4. <b>Objective 4:</b> Evaluate system performance through comprehensive testing",
    ]
    for obj in specific_objectives:
        elements.append(Paragraph(obj, normal_style))

    elements.append(Paragraph("1.4 Scope and Limitations", heading2_style))
    elements.append(
        Paragraph(
            "This project focuses on developing a proof-of-concept system that demonstrates the "
            "feasibility of the proposed approach. The following aspects are within scope:",
            normal_style,
        )
    )
    scope_items = [
        "• Core system functionality and user interface",
        "• Document processing and information extraction",
        "• AI-powered content generation",
        "• Basic security and authentication",
    ]
    for item in scope_items:
        elements.append(Paragraph(item, normal_style))

    elements.append(Paragraph("The following limitations apply:", normal_style))
    limitations = [
        "• Limited to specific document formats (PDF, text)",
        "• Requires internet connectivity for AI features",
        "• Not optimized for mobile devices",
    ]
    for limitation in limitations:
        elements.append(Paragraph(limitation, normal_style))

    elements.append(PageBreak())

    # Chapter 2: Literature Review
    elements.append(Paragraph("Chapter 2: Literature Review", heading1_style))

    elements.append(Paragraph("2.1 Theoretical Framework", heading2_style))
    elements.append(
        Paragraph(
            "The theoretical foundation of this work is based on information retrieval theory and "
            "natural language processing principles. Key concepts include semantic similarity, "
            "vector embeddings, and transformer-based language models. The relationship between "
            "document representation and retrieval effectiveness is particularly relevant to this project.",
            normal_style,
        )
    )

    elements.append(Paragraph("2.2 Related Work", heading2_style))
    elements.append(
        Paragraph(
            "Several researchers have addressed similar problems in recent years. Smith et al. (2023) "
            "proposed a document processing system using deep learning, which achieved 92% accuracy. "
            "Johnson and Lee (2024) developed a semantic search engine demonstrating significant "
            "improvements over keyword-based approaches. Chen et al. (2023) investigated automated "
            "content generation, concluding that transformer models outperform traditional methods.",
            normal_style,
        )
    )

    elements.append(Paragraph("2.3 Comparative Analysis", heading2_style))
    elements.append(
        Paragraph(
            "A comparison of existing approaches reveals the following:", normal_style
        )
    )
    elements.append(
        Paragraph(
            "<b>Traditional Keyword-Based Systems:</b><br/>"
            "Strengths: Fast, simple to implement, low computational requirements<br/>"
            "Weaknesses: Limited understanding of context, poor handling of synonyms<br/>"
            "Applicability: Suitable for simple search tasks",
            normal_style,
        )
    )
    elements.append(
        Paragraph(
            "<b>Modern AI-Powered Systems:</b><br/>"
            "Strengths: Context-aware, handles semantic similarity, high accuracy<br/>"
            "Weaknesses: Higher computational cost, requires training data<br/>"
            "Applicability: Ideal for complex information retrieval tasks",
            normal_style,
        )
    )

    elements.append(Paragraph("2.4 Research Gap", heading2_style))
    elements.append(
        Paragraph(
            "Despite the progress made in document processing and information retrieval, there remains "
            "a gap in integrated systems that combine multiple AI capabilities in a user-friendly "
            "interface. This project aims to fill this gap by developing a comprehensive solution that "
            "brings together document processing, semantic search, and intelligent content generation.",
            normal_style,
        )
    )

    elements.append(PageBreak())

    # Chapter 3: Methodology and System Design
    elements.append(
        Paragraph("Chapter 3: Methodology and System Design", heading1_style)
    )

    elements.append(Paragraph("3.1 Research Methodology", heading2_style))
    elements.append(
        Paragraph(
            "This project follows an iterative development approach. The research process consists "
            "of the following phases:",
            normal_style,
        )
    )
    phases = [
        "<b>Phase 1: Requirements Analysis</b> - Identify stakeholder needs and define system requirements",
        "<b>Phase 2: Design</b> - Create system architecture and detailed component designs",
        "<b>Phase 3: Implementation</b> - Develop core components and integrate modules",
        "<b>Phase 4: Evaluation</b> - Conduct testing and analyze results",
    ]
    for phase in phases:
        elements.append(Paragraph(phase, normal_style))

    elements.append(Paragraph("3.2 System Architecture", heading2_style))
    elements.append(
        Paragraph(
            "The system architecture consists of three main layers:", normal_style
        )
    )
    layers = [
        "<b>Presentation Layer:</b> User interface components, input validation, output formatting",
        "<b>Business Logic Layer:</b> Core application logic, business rules, data processing",
        "<b>Data Access Layer:</b> Database operations, data persistence, query optimization",
    ]
    for layer in layers:
        elements.append(Paragraph(layer, normal_style))

    elements.append(Paragraph("3.3 Design Specifications", heading2_style))
    elements.append(
        Paragraph(
            "The system is designed with the following key specifications:",
            normal_style,
        )
    )
    specs = [
        "<b>FR1:</b> The system shall support user authentication and authorization",
        "<b>FR2:</b> The system shall process PDF documents and extract text content",
        "<b>FR3:</b> The system shall provide semantic search capabilities",
        "<b>FR4:</b> The system shall generate content using AI models",
        "<b>NFR1:</b> The system shall respond to user requests within 2 seconds",
        "<b>NFR2:</b> The system shall support at least 100 concurrent users",
        "<b>NFR3:</b> The system shall maintain 99.9% uptime",
    ]
    for spec in specs:
        elements.append(Paragraph(spec, normal_style))

    elements.append(Paragraph("3.4 Tools and Technologies", heading2_style))
    elements.append(
        Paragraph(
            "The following tools and technologies are used in this project:",
            normal_style,
        )
    )
    tech = [
        "<b>Backend:</b> Python, FastAPI, SQLAlchemy, Celery",
        "<b>Frontend:</b> React, TypeScript, Tailwind CSS",
        "<b>Database:</b> PostgreSQL, Redis, Qdrant",
        "<b>AI/ML:</b> OpenAI GPT-4, Sentence Transformers",
        "<b>Infrastructure:</b> Docker, MinIO",
    ]
    for t in tech:
        elements.append(Paragraph(t, normal_style))

    elements.append(PageBreak())

    # Chapter 4: Implementation
    elements.append(Paragraph("Chapter 4: Implementation", heading1_style))

    elements.append(Paragraph("4.1 Development Environment", heading2_style))
    elements.append(
        Paragraph(
            "The development environment consists of modern tools and frameworks that facilitate "
            "efficient development and testing. Version control is managed using Git, and the project "
            "follows standard coding conventions and best practices.",
            normal_style,
        )
    )

    elements.append(Paragraph("4.2 Implementation Details", heading2_style))
    elements.append(
        Paragraph(
            "The implementation follows the design specifications outlined in Chapter 3. Key modules include:",
            normal_style,
        )
    )
    modules = [
        "<b>Authentication Module:</b> Handles user registration, login, and session management using JWT tokens",
        "<b>Document Processing Module:</b> Extracts text from PDFs, performs OCR on images, and structures content",
        "<b>Search Module:</b> Implements semantic search using vector embeddings and Qdrant database",
        "<b>Content Generation Module:</b> Integrates with OpenAI API to generate contextual content",
        "<b>Export Module:</b> Generates PDF and DOCX files with proper formatting",
    ]
    for module in modules:
        elements.append(Paragraph(module, normal_style))

    elements.append(Paragraph("4.3 Testing and Validation", heading2_style))
    elements.append(
        Paragraph(
            "Comprehensive testing was conducted at multiple levels:", normal_style
        )
    )
    testing = [
        "<b>Unit Testing:</b> Individual components tested in isolation with 85% code coverage",
        "<b>Integration Testing:</b> Module interactions verified through automated test suites",
        "<b>System Testing:</b> End-to-end workflows validated with real-world scenarios",
        "<b>User Acceptance Testing:</b> Feedback collected from target users",
    ]
    for test in testing:
        elements.append(Paragraph(test, normal_style))

    elements.append(Paragraph("4.4 Challenges and Solutions", heading2_style))
    elements.append(
        Paragraph(
            "Several challenges were encountered during implementation:", normal_style
        )
    )
    challenges_solutions = [
        "<b>Challenge 1:</b> Handling large PDF files efficiently<br/>"
        "<b>Solution:</b> Implemented asynchronous processing using Celery workers",
        "<b>Challenge 2:</b> Ensuring accurate text extraction from scanned documents<br/>"
        "<b>Solution:</b> Integrated Tesseract OCR with image preprocessing",
        "<b>Challenge 3:</b> Optimizing semantic search performance<br/>"
        "<b>Solution:</b> Used Qdrant vector database with optimized indexing",
    ]
    for cs in challenges_solutions:
        elements.append(Paragraph(cs, normal_style))

    elements.append(PageBreak())

    # Chapter 5: Results and Discussion
    elements.append(Paragraph("Chapter 5: Results and Discussion", heading1_style))

    elements.append(Paragraph("5.1 Experimental Setup", heading2_style))
    elements.append(
        Paragraph(
            "The experiments were conducted on a system with the following specifications: "
            "Intel Core i7 processor, 16GB RAM, Windows 11. The test dataset consisted of "
            "100 PDF documents covering various topics. Evaluation metrics included accuracy, "
            "response time, and user satisfaction scores.",
            normal_style,
        )
    )

    elements.append(Paragraph("5.2 Results Analysis", heading2_style))
    elements.append(
        Paragraph(
            "The system demonstrated strong performance across all evaluation metrics:",
            normal_style,
        )
    )
    results = [
        "<b>Document Processing:</b> Successfully processed 98% of test documents with average time of 3.2 seconds",
        "<b>Search Accuracy:</b> Achieved 91% precision and 89% recall in semantic search tasks",
        "<b>Content Generation:</b> Generated relevant content with 87% user approval rating",
        "<b>System Response Time:</b> Average response time of 1.8 seconds, meeting the 2-second requirement",
    ]
    for result in results:
        elements.append(Paragraph(result, normal_style))

    elements.append(Paragraph("5.3 Performance Evaluation", heading2_style))
    elements.append(
        Paragraph(
            "Compared to baseline systems, the proposed solution shows significant improvements:",
            normal_style,
        )
    )
    comparisons = [
        "• 35% faster document processing compared to traditional methods",
        "• 42% improvement in search relevance over keyword-based systems",
        "• 28% reduction in time required to create reports",
    ]
    for comp in comparisons:
        elements.append(Paragraph(comp, normal_style))

    elements.append(Paragraph("5.4 Discussion", heading2_style))
    elements.append(
        Paragraph(
            "The results demonstrate that the proposed system effectively addresses the identified "
            "challenges. The integration of AI-powered features significantly enhances user productivity "
            "and content quality. The semantic search capability proves particularly valuable in finding "
            "relevant information across large document collections.",
            normal_style,
        )
    )
    elements.append(
        Paragraph(
            "The main strengths of the system include its comprehensive feature set, user-friendly "
            "interface, and strong performance. However, some limitations exist, such as dependency "
            "on external AI services and the need for internet connectivity.",
            normal_style,
        )
    )

    elements.append(PageBreak())

    # Chapter 6: Conclusion and Future Work
    elements.append(Paragraph("Chapter 6: Conclusion and Future Work", heading1_style))

    elements.append(Paragraph("6.1 Summary of Achievements", heading2_style))
    elements.append(
        Paragraph(
            "This project successfully achieved all stated objectives:", normal_style
        )
    )
    achievements = [
        "• Designed and implemented a scalable system architecture",
        "• Developed automated document processing capabilities",
        "• Integrated AI-powered semantic search and content generation",
        "• Validated system performance through comprehensive testing",
    ]
    for achievement in achievements:
        elements.append(Paragraph(achievement, normal_style))

    elements.append(Paragraph("6.2 Contributions", heading2_style))
    elements.append(
        Paragraph("This project makes the following contributions:", normal_style)
    )
    contributions = [
        "<b>Theoretical:</b> Demonstrates effective integration of multiple AI technologies",
        "<b>Practical:</b> Provides a working solution that improves productivity",
        "<b>Technical:</b> Offers reusable components and design patterns",
    ]
    for contrib in contributions:
        elements.append(Paragraph(contrib, normal_style))

    elements.append(Paragraph("6.3 Future Work", heading2_style))
    elements.append(Paragraph("Future research directions include:", normal_style))
    future_work = [
        "<b>Short-term:</b> Add support for more document formats, improve mobile responsiveness",
        "<b>Medium-term:</b> Implement collaborative editing features, add version control",
        "<b>Long-term:</b> Develop offline capabilities, create mobile applications",
    ]
    for fw in future_work:
        elements.append(Paragraph(fw, normal_style))

    elements.append(PageBreak())

    # General Conclusion
    elements.append(Paragraph("General Conclusion", heading1_style))
    elements.append(
        Paragraph(
            "This project addressed the challenge of inefficient information management by developing "
            "an intelligent system that automates document processing and content generation. Through "
            "a systematic approach involving requirements analysis, design, implementation, and testing, "
            "we created a comprehensive solution that leverages modern AI technologies.",
            normal_style,
        )
    )
    elements.append(
        Paragraph(
            "The results demonstrate significant improvements in productivity and content quality. "
            "The system successfully processes documents, provides semantic search capabilities, and "
            "generates relevant content using AI. User feedback has been overwhelmingly positive, "
            "with particular praise for the intuitive interface and powerful features.",
            normal_style,
        )
    )
    elements.append(
        Paragraph(
            "This work contributes to the field of intelligent information systems by demonstrating "
            "how multiple AI technologies can be effectively integrated into a cohesive solution. "
            "The findings have implications for organizations seeking to improve their document "
            "management and content creation workflows.",
            normal_style,
        )
    )
    elements.append(
        Paragraph(
            "Looking forward, there are several promising directions for future research, including "
            "enhanced collaboration features, offline capabilities, and mobile applications. With "
            "continued development, this work has the potential to transform how professionals create "
            "and manage reports.",
            normal_style,
        )
    )

    elements.append(PageBreak())

    # Bibliography
    elements.append(Paragraph("Bibliography / References", heading1_style))
    references = [
        "[1] Smith, J., Brown, A., & Davis, M. (2023). Deep Learning for Document Processing. "
        "Journal of Artificial Intelligence Research, 45(2), 123-145.",
        "[2] Johnson, R., & Lee, S. (2024). Semantic Search Engines: A Comprehensive Review. "
        "ACM Computing Surveys, 56(1), 1-34.",
        "[3] Chen, L., Wang, Y., & Zhang, H. (2023). Automated Content Generation Using "
        "Transformer Models. In Proceedings of the International Conference on Natural Language "
        "Processing (pp. 456-467). New York: ACM Press.",
        "[4] Williams, K. (2023). Modern Web Application Development with React and TypeScript. "
        "O'Reilly Media.",
        "[5] Garcia, M., & Rodriguez, P. (2024). Vector Databases for Semantic Search. "
        "IEEE Transactions on Knowledge and Data Engineering, 36(3), 789-802.",
        "[6] OpenAI. (2024). GPT-4 Technical Report. Retrieved from https://openai.com/research/gpt-4",
        "[7] Anderson, T. (2023). Building Scalable Systems with FastAPI and Python. "
        "Technical Report TR-2023-05, Stanford University.",
        "[8] Kumar, S., & Patel, N. (2024). User Experience Design for AI-Powered Applications. "
        "In Miller, D. (Ed.), Human-Computer Interaction Handbook (pp. 234-256). Springer.",
    ]
    for ref in references:
        elements.append(Paragraph(ref, normal_style))

    elements.append(PageBreak())

    # Appendices
    elements.append(Paragraph("Appendices", heading1_style))

    elements.append(Paragraph("Appendix A: System Requirements", heading2_style))
    elements.append(
        Paragraph(
            "<b>Hardware Requirements:</b><br/>"
            "• Processor: Intel Core i5 or equivalent<br/>"
            "• RAM: 8GB minimum, 16GB recommended<br/>"
            "• Storage: 10GB available space<br/>"
            "• Network: Broadband internet connection",
            normal_style,
        )
    )
    elements.append(
        Paragraph(
            "<b>Software Requirements:</b><br/>"
            "• Operating System: Windows 10/11, macOS 10.15+, or Linux<br/>"
            "• Python 3.11 or higher<br/>"
            "• Node.js 18 or higher<br/>"
            "• Docker Desktop<br/>"
            "• Modern web browser (Chrome, Firefox, Safari, Edge)",
            normal_style,
        )
    )

    elements.append(Paragraph("Appendix B: Installation Guide", heading2_style))
    elements.append(
        Paragraph(
            "1. Clone the repository from GitHub<br/>"
            "2. Install Docker Desktop and start Docker services<br/>"
            "3. Run docker-compose up -d to start infrastructure<br/>"
            "4. Install Python dependencies: pip install -r requirements.txt<br/>"
            "5. Install Node.js dependencies: npm install<br/>"
            "6. Configure environment variables in .env file<br/>"
            "7. Run database migrations: alembic upgrade head<br/>"
            "8. Start backend server: uvicorn app.main:app --reload<br/>"
            "9. Start Celery worker: celery -A app.worker.celery_app worker<br/>"
            "10. Start frontend: npm run dev",
            normal_style,
        )
    )

    elements.append(Paragraph("Appendix C: User Guide", heading2_style))
    elements.append(
        Paragraph(
            "<b>Getting Started:</b><br/>"
            "1. Register for an account using your email address<br/>"
            "2. Log in with your credentials<br/>"
            "3. Create a new report from the dashboard<br/>"
            "4. Upload a template PDF (optional)<br/>"
            "5. Upload note files for reference<br/>"
            "6. Use semantic search to find relevant information<br/>"
            "7. Generate content for report sections<br/>"
            "8. Edit and refine the generated content<br/>"
            "9. Export your report to PDF or DOCX format",
            normal_style,
        )
    )

    # Build PDF
    doc.build(elements)
    print(f"✅ PDF template created successfully: {filename}")
    print(f"📄 File size: {os.path.getsize(filename) / 1024:.2f} KB")
    print(f"📍 Location: {os.path.abspath(filename)}")


if __name__ == "__main__":
    import os

    create_test_template()
