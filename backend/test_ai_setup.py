"""
Test script to verify AI infrastructure setup
Run this to check if all AI services are working correctly
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def test_imports():
    """Test if all required packages are installed"""
    print("=" * 60)
    print("Testing Package Imports...")
    print("=" * 60)

    try:
        import sentence_transformers

        print("✅ sentence-transformers installed")
    except ImportError:
        print("❌ sentence-transformers NOT installed")
        print("   Run: pip install sentence-transformers")
        return False

    try:
        import qdrant_client

        print("✅ qdrant-client installed")
    except ImportError:
        print("❌ qdrant-client NOT installed")
        print("   Run: pip install qdrant-client")
        return False

    try:
        import openai

        print("✅ openai installed")
    except ImportError:
        print("❌ openai NOT installed")
        print("   Run: pip install openai")
        return False

    try:
        import tiktoken

        print("✅ tiktoken installed")
    except ImportError:
        print("❌ tiktoken NOT installed")
        print("   Run: pip install tiktoken")
        return False

    print("\n✅ All required packages are installed!\n")
    return True


def test_embedding_service():
    """Test embedding generation"""
    print("=" * 60)
    print("Testing Embedding Service...")
    print("=" * 60)

    try:
        from app.services.embedding_service import get_embedding_service

        print("Initializing embedding service (downloading model if needed)...")
        embedding_service = get_embedding_service()

        print(f"✅ Model loaded: {embedding_service.embedding_dim} dimensions")

        # Test single embedding
        text = "This is a test note about machine learning and artificial intelligence."
        print(f"\nGenerating embedding for: '{text[:50]}...'")
        embedding = embedding_service.generate_embedding(text)
        print(f"✅ Generated embedding: {len(embedding)} dimensions")
        print(f"   First 5 values: {embedding[:5]}")

        # Test chunking
        long_text = " ".join(["This is sentence number " + str(i) for i in range(100)])
        chunks = embedding_service.chunk_text(long_text, max_tokens=50)
        print(f"\n✅ Text chunking works: {len(chunks)} chunks from long text")

        # Test batch processing
        texts = [
            "Machine learning is a subset of artificial intelligence.",
            "Deep learning uses neural networks with multiple layers.",
            "Natural language processing helps computers understand text.",
        ]
        print(f"\nGenerating embeddings for {len(texts)} texts...")
        embeddings = embedding_service.generate_embeddings_batch(texts)
        print(f"✅ Batch processing works: {len(embeddings)} embeddings generated")

        print("\n✅ Embedding Service is working correctly!\n")
        return True

    except Exception as e:
        print(f"\n❌ Embedding Service Error: {e}\n")
        return False


def test_vector_service():
    """Test vector database connection"""
    print("=" * 60)
    print("Testing Vector Service (Qdrant)...")
    print("=" * 60)

    try:
        from app.services.vector_service import get_vector_service
        from app.services.embedding_service import get_embedding_service

        print("Connecting to Qdrant...")
        vector_service = get_vector_service()
        print("✅ Connected to Qdrant")
        print(f"   Collection: {vector_service.collection_name}")
        print(f"   Embedding dimension: {vector_service.embedding_dim}")

        # Test storing an embedding
        embedding_service = get_embedding_service()
        text = "Test note about Python programming and web development."
        embedding = embedding_service.generate_embedding(text)

        print(f"\nStoring test embedding...")
        point_id = vector_service.store_embedding(
            embedding=embedding,
            note_id=999,
            chunk_index=0,
            chunk_text=text,
            report_id=1,
            user_id=1,
            filename="test.txt",
            file_type="txt",
        )
        print(f"✅ Stored embedding with ID: {point_id}")

        # Test searching
        print(f"\nSearching for similar content...")
        query_text = "Python web development"
        query_embedding = embedding_service.generate_embedding(query_text)
        results = vector_service.search_similar(
            query_embedding=query_embedding, report_id=1, user_id=1, limit=5
        )
        print(f"✅ Search works: Found {len(results)} results")
        if results:
            print(f"   Top result score: {results[0]['score']:.4f}")
            print(f"   Top result text: {results[0]['chunk_text'][:60]}...")

        # Cleanup
        print(f"\nCleaning up test data...")
        vector_service.delete_note_embeddings(999)
        print(f"✅ Cleanup complete")

        print("\n✅ Vector Service is working correctly!\n")
        return True

    except Exception as e:
        print(f"\n❌ Vector Service Error: {e}")
        print("\nMake sure Qdrant is running:")
        print("   docker run -p 6333:6333 qdrant/qdrant")
        print()
        return False


def test_content_generation_service():
    """Test content generation (requires OpenAI API key)"""
    print("=" * 60)
    print("Testing Content Generation Service...")
    print("=" * 60)

    try:
        from app.core.config import settings

        if not settings.OPENAI_API_KEY or settings.OPENAI_API_KEY == "":
            print("⚠️  OpenAI API key not configured")
            print("   Set OPENAI_API_KEY in .env file to test content generation")
            print("   Skipping content generation test...\n")
            return True

        from app.services.content_generation_service import (
            get_content_generation_service,
        )
        from app.services.embedding_service import get_embedding_service
        from app.services.vector_service import get_vector_service

        print("Initializing content generation service...")
        content_service = get_content_generation_service()
        print(f"✅ Service initialized with model: {content_service.model}")

        # Set up test data
        print("\nSetting up test data...")
        embedding_service = get_embedding_service()
        vector_service = get_vector_service()

        # Add some test notes
        test_notes = [
            "Machine learning is a method of data analysis that automates analytical model building.",
            "Deep learning is part of a broader family of machine learning methods based on artificial neural networks.",
            "Supervised learning uses labeled datasets to train algorithms to classify data or predict outcomes.",
        ]

        for idx, note_text in enumerate(test_notes):
            embedding = embedding_service.generate_embedding(note_text)
            vector_service.store_embedding(
                embedding=embedding,
                note_id=1000 + idx,
                chunk_index=0,
                chunk_text=note_text,
                report_id=2,
                user_id=2,
                filename=f"test_note_{idx}.txt",
                file_type="txt",
            )
        print(f"✅ Added {len(test_notes)} test notes")

        # Test content generation
        print("\nGenerating content (this may take a few seconds)...")
        result = content_service.generate_section_content(
            section_title="Introduction to Machine Learning",
            section_description="Provide an overview of machine learning concepts",
            report_id=2,
            user_id=2,
        )

        print(f"\n✅ Content generated successfully!")
        print(f"\n{'='*60}")
        print("Generated Content:")
        print(f"{'='*60}")
        print(
            result["content"][:500] + "..."
            if len(result["content"]) > 500
            else result["content"]
        )
        print(f"\n{'='*60}")
        print("Metadata:")
        print(f"{'='*60}")
        print(f"Model: {result['metadata']['model']}")
        print(f"Input tokens: {result['metadata']['input_tokens']}")
        print(f"Output tokens: {result['metadata']['output_tokens']}")
        print(f"Total tokens: {result['metadata']['total_tokens']}")
        print(f"Estimated cost: ${result['metadata']['estimated_cost']}")
        print(f"Sources used: {len(result['sources'])}")

        # Cleanup
        print(f"\nCleaning up test data...")
        for idx in range(len(test_notes)):
            vector_service.delete_note_embeddings(1000 + idx)
        print(f"✅ Cleanup complete")

        print("\n✅ Content Generation Service is working correctly!\n")
        return True

    except Exception as e:
        print(f"\n❌ Content Generation Service Error: {e}\n")
        import traceback

        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("AI Infrastructure Test Suite")
    print("=" * 60 + "\n")

    results = []

    # Test 1: Package imports
    results.append(("Package Imports", test_imports()))

    if not results[0][1]:
        print("\n❌ Cannot proceed without required packages installed")
        print("   Run: pip install -r requirements-minimal.txt")
        return

    # Test 2: Embedding service
    results.append(("Embedding Service", test_embedding_service()))

    # Test 3: Vector service
    results.append(("Vector Service", test_vector_service()))

    # Test 4: Content generation
    results.append(("Content Generation", test_content_generation_service()))

    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)

    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {test_name}")

    all_passed = all(result[1] for result in results)

    if all_passed:
        print("\n🎉 All tests passed! AI infrastructure is ready!")
        print("\nNext steps:")
        print("1. Create API endpoints to expose these services")
        print("2. Integrate with frontend")
        print("3. Test end-to-end flow")
    else:
        print("\n⚠️  Some tests failed. Please fix the issues above.")

    print()


if __name__ == "__main__":
    main()
