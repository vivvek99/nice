## 📚🔍 Ask NICE

Ask any medical question and get a beautiful explanation with the [NICE Clinical Knowledge Summaries](https://cks.nice.org.uk/) as the source. You can even clear your PLAB or MRCP MCQ doubts.

### Disclaimer
DO NOT use as a substitute for professional medical advice. This is a work in progress meant for **EDUCATIONAL PURPOSES ONLY**.

### 📚 Technical description

📄 The app implements the following academic papers:

- [In-Context Retrieval-Augmented Language Models](https://arxiv.org/abs/2302.00083) aka **RALM**
  - The idea of retrieval augmented generation is that when given a question you first do a retrieval step to fetch any relevant documents (in this case, [NICE Clinical Knowledge Summaries](https://cks.nice.org.uk/)). You then pass those documents, along with the original question, to the language model and have it generate a response
- [Precise Zero-Shot Dense Retrieval without Relevance Labels](https://arxiv.org/abs/2212.10496) aka **HyDE** (Hypothetical Document Embeddings)
  - HyDE is an embedding technique that takes queries, generates a hypothetical answer, and then embeds that generated document to fetch documents more accurately

Question-Answering has the following steps, all handled by [RetrievalQAWithSourcesChain](https://python.langchain.com/en/latest/modules/chains/index_examples/vector_db_qa_with_sources.html):

1. Given a user question, create a hypothetical answer (possibly false, with factual inaccuracies) and then store that as Embeddings.
2. Look up relevant documents from the vectorstore using Embeddings and a similarity search.
3. Pass the user question and relevant documents to GPT-3.5-turbo to generate a final answer.

Here's a visual representation of how it all works: