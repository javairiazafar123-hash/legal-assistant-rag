import streamlit as st
from typing import List, Dict

class SimpleRAG:
    def __init__(self):
        self.knowledge_base = [
            "Statute of limitations for contracts: Generally 4-6 years from breach date",
            "For personal injury cases: 2-3 years from date of injury",
            "Intellectual property rights: Copyright lasts for author's lifetime + 70 years",
            "Patents: Valid for 20 years from filing date",
            "Contract law: Requires offer, acceptance, consideration, and mutual intent",
            "Tort law: Covers negligence, intentional harm, and strict liability",
            "Criminal law: Prosecution must prove guilt beyond reasonable doubt",
        ]
    
    def add_document(self, text: str) -> bool:
        if text.strip():
            self.knowledge_base.append(text)
            return True
        return False
    
    def search(self, query: str, top_k: int = 3) -> Dict:
        if not query.strip():
            return {"answer": "Please enter a question.", "sources": [], "confidence": 0.0}
        
        query_lower = query.lower()
        query_words = set(query_lower.split())
        
        scored_docs = []
        for doc in self.knowledge_base:
            doc_lower = doc.lower()
            doc_words = set(doc_lower.split())
            overlap = len(query_words & doc_words)
            if overlap > 0:
                scored_docs.append((doc, overlap))
        
        scored_docs.sort(key=lambda x: x[1], reverse=True)
        top_docs = [doc for doc, _ in scored_docs[:top_k]]
        
        if not top_docs:
            return {"answer": "No relevant documents found.", "sources": [], "confidence": 0.0}
        
        answer = self._generate_answer(query, top_docs)
        confidence = min(1.0, len(scored_docs) / 20)
        
        return {"answer": answer, "sources": top_docs, "confidence": confidence}
    
    def _generate_answer(self, query: str, sources: List[str]) -> str:
        context = "\n\n".join(f"• {doc}" for doc in sources)
        return f"**Legal Information:**\n\n{context}\n\n⚖️ *For specific legal advice, consult a qualified attorney.*"

def main():
    st.set_page_config(page_title="Legal Assistant", page_icon="⚖️", layout="wide")
    
    if "rag" not in st.session_state:
        st.session_state.rag = SimpleRAG()
    
    rag = st.session_state.rag
    
    st.title("⚖️ Legal Assistant")
    st.markdown("Your AI-powered legal information system")
    st.markdown("---")
    
    with st.sidebar:
        st.header("📚 Knowledge Base")
        st.metric("Documents", len(rag.knowledge_base))
        
        st.markdown("---")
        st.header("➕ Add Document")
        custom_doc = st.text_area("Add legal text:", height=100)
        if st.button("Add"):
            if rag.add_document(custom_doc):
                st.success(f"✅ Added! Total: {len(rag.knowledge_base)}")
    
    st.subheader("🔍 Ask a Question")
    question = st.text_input("Your question:", placeholder="E.g., What is statute of limitations?")
    
    if st.button("Search", type="primary"):
        if question:
            result = rag.search(question, top_k=3)
            st.success("Found!")
            st.markdown(result["answer"])
            st.metric("Confidence", f"{result['confidence']:.0%}")
            if result['sources']:
                with st.expander("Sources"):
                    for source in result['sources']:
                        st.write(f"• {source}")
    
    st.markdown("---")
    st.caption("⚠️ For legal advice, consult a licensed attorney.")

if __name__ == "__main__":
    main()
