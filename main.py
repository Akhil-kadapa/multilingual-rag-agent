from document_loader import load_documents, chunk_text
from embeddings import create_embeddings, store_embeddings
from retriever import retrieve_chunks
from generator import generate_answer, summarize_document, evaluate_answer

def select_language():
    """
    Lets user select output language
    """
    print("\nSelect output language:")
    print("1. English")
    print("2. Telugu")
    print("3. Hindi")
    print("4. French")
    print("5. Spanish")
    
    languages = {
        "1": "English",
        "2": "Telugu",
        "3": "Hindi",
        "4": "French",
        "5": "Spanish"
    }
    
    choice = input("\nEnter choice (1-5): ")
    return languages.get(choice, "English")

def main():
    """
    Main function that runs the knowledge base agent
    """
    print("Welcome to Multilingual RAG System Agent!")
    print("Loading documents...")
    
    # Step 1 - Load documents
    documents = load_documents("documents/")
    
    if len(documents) == 0:
        print("No documents found in documents/ folder!")
        return
    
    print(f"Loaded {len(documents)} documents")

    # Step 5 - Select Language
    language = select_language()
    print(f"Output language set to: {language}")
    print("Ready! Ask your questions.")
    print("Type 'quit' to exit")
    print("Type 'language' anytime to change language\n")

    # Show document summaries
    print("\n📄 Document Summaries:")
    print("━" * 40)
    for doc in documents:
        print(f"\n📌 {doc['filename']}")
        summary = summarize_document(doc['text'], doc['filename'], language)
        print(f"Summary: {summary}")
    print("━" * 40)
    print("Now you know what's in your documents!\n")
    
    # Step 2 - Chunk documents
    print("Chunking documents...")
    all_chunks = []
    for doc in documents:
        chunks = chunk_text(doc["text"], doc["filename"])
        all_chunks.extend(chunks)
    
    print(f"Created {len(all_chunks)} chunks")
    
    # Step 3 - Create embeddings
    print("Creating embeddings...")
    embeddings = create_embeddings(all_chunks)
    
    # Step 4 - Store in FAISS
    print("Storing in vector database...")
    index, chunks = store_embeddings(embeddings, all_chunks)
    # Step 5 - Select Language
    #language = select_language()
    #print(f"Output language set to: {language}")
    #print("Ready! Ask your questions.")
    #print("Type 'quit' to exit")
    #print("Type 'language' anytime to change language\n")

    while True:
        question = input("Your question: ")
    
        if question.lower() == "quit":
            break
    
        if question.lower() == "language":
            language = select_language()
            print(f"Output language changed to: {language}\n")
            continue
    
        relevant_chunks = retrieve_chunks(question, index, chunks)
        result = generate_answer(question, relevant_chunks, language)
    
        print(f"\nAnswer: {result['answer']}")
        print(f"Sources: {result['sources']}")

        # Evaluate the answer
        evaluation = evaluate_answer(question, result['answer'], relevant_chunks)

        print(f"\n📊 Answer Evaluation:")
        print(f"Faithfulness Score: {evaluation['faithfulness_score']}/100")
        print(f"Retrieval Quality: {evaluation['retrieval_quality']}")
        print(f"Problem Area: {evaluation['problem_area']}")
        print(f"Diagnosis: {evaluation['diagnosis']}\n")
if __name__ == "__main__":
    main()