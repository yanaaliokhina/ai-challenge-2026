from template import PromptTemplate
from library import TemplateLibrary

library = TemplateLibrary()

library.register(
    "translate",
    PromptTemplate("Translate the following text into {language}:\n\n{text}"),
)

library.register(
    "summarise",
    PromptTemplate("Summarise the following text in {num_sentences} sentences:\n\n{text}"),
)

library.register(
    "qa",
    PromptTemplate(
        "Context:\n{context}\n\nQuestion: {question}\n\nAnswer:"
    ),
)
