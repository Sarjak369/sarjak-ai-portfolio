# Research Publications

I have authored and published two research papers in the fields of Natural Language Processing and Educational Technology.

---

## Publication 1: To Laugh or Not to Laugh – LSTM Based Humor Detection Approach

### Overview

This research addresses the challenging problem of automatically detecting humor in text using deep learning techniques. Humor detection is a complex NLP task because humor often relies on context, wordplay, cultural knowledge, and subtle linguistic cues.

### Problem Statement

Traditional rule-based approaches to humor detection fail to capture the nuanced and context-dependent nature of humor. We needed a more sophisticated approach that could learn patterns from data.

### Our Approach

We developed an LSTM (Long Short-Term Memory) based neural network architecture specifically designed for humor detection in text.

**Key Components:**

- **Text Preprocessing**: Tokenization, cleaning, and normalization
- **Feature Extraction**: Linguistic features, semantic embeddings, context windows
- **LSTM Architecture**: Multi-layer LSTM network to capture sequential dependencies
- **Classification Layer**: Binary classification (humorous vs. non-humorous)

### Technical Details

**Model Architecture:**

- Embedding layer for word representations
- Bidirectional LSTM layers to capture context from both directions
- Attention mechanism to focus on key humor indicators
- Dense layers for final classification

**Dataset:**

- Collected from multiple sources (social media, jokes databases, regular text)
- Balanced dataset to avoid bias
- Train/validation/test split for robust evaluation

**Features Used:**

- Word embeddings (Word2Vec, GloVe)
- Part-of-speech tags
- Syntactic patterns
- Semantic incongruity features
- Context length and complexity

### Results

- Achieved significant improvement over baseline approaches
- Successfully identified various types of humor (wordplay, irony, sarcasm)
- Model demonstrated robustness across different humor styles

### Challenges Addressed

1. **Subjectivity**: Humor is subjective—what's funny to one person may not be to another
2. **Context Dependency**: Humor often requires understanding broader context
3. **Cultural Variations**: Humor varies across cultures and languages
4. **Data Scarcity**: Limited labeled datasets for humor detection

### Applications

- Social media content moderation
- Chatbot personality enhancement
- Sentiment analysis enhancement
- Creative writing assistance

### Technical Skills Demonstrated

- Deep learning (LSTM, RNNs)
- Natural Language Processing
- TensorFlow/PyTorch
- Feature engineering
- Model evaluation and validation
- Research methodology

---

## Publication 2: Generation and Grading of Arduous MCQs Using NLP and OMR Detection Using OpenCV

### Overview

This research presents an end-to-end automated system for generating challenging multiple-choice questions (MCQs) from text and grading answer sheets using computer vision techniques.

### Problem Statement

Creating high-quality, difficulty-calibrated MCQs is time-consuming for educators. Additionally, manual grading of MCQ answer sheets is tedious and error-prone. We needed an automated solution for both challenges.

### System Architecture

**Part 1: Automated MCQ Generation**

**Input:** Text corpus (textbooks, articles, lecture notes)

**Process:**

1. **Text Analysis**: Extract key concepts and facts using NLP
2. **Question Generation**: Create questions from important sentences
3. **Distractor Generation**: Generate plausible incorrect options
4. **Difficulty Assessment**: Assign difficulty levels based on complexity metrics

**Techniques Used:**

- Named Entity Recognition (NER) for identifying key terms
- Dependency parsing for understanding sentence structure
- Semantic similarity for distractor generation
- Rule-based and neural approaches combined

**Part 2: OMR Detection and Grading**

**Input:** Scanned answer sheets

**Process:**
1. **Image Preprocessing**: Enhance image quality, correct skew
2. **OMR Detection**: Identify marked bubbles using OpenCV
3. **Answer Extraction**: Convert marks to answer choices
4. **Grading**: Compare with answer key and calculate scores

**Techniques Used:**

- OpenCV for computer vision tasks
- Contour detection for bubble identification
- Thresholding and morphological operations
- Perspective transformation for skew correction

### Technical Details

**NLP Pipeline:**

```bash
Text Input → Sentence Tokenization → POS Tagging → 
NER → Relation Extraction → Question Template Matching → 
Distractor Generation → Difficulty Assessment → MCQ Output
```

**Computer Vision Pipeline:**

```bash
Scanned Image → Preprocessing → Bubble Detection → 
Mark Recognition → Answer Extraction → Grading → Result Output
```

**Difficulty Calibration:**

We developed metrics to assess question difficulty:
- Concept complexity (using word embeddings)
- Distractor plausibility (semantic similarity with correct answer)
- Prerequisite knowledge requirements
- Cognitive level (Bloom's taxonomy)

### Results

**MCQ Generation:**

- Generated contextually relevant questions
- Maintained grammatical correctness
- Produced plausible distractors
- Successfully calibrated difficulty levels

**OMR Grading:**

- High accuracy in bubble detection (>95%)
- Robust to various scanning conditions
- Handled skewed and rotated images
- Fast processing (<1 second per sheet)

### Applications

1. **Educational Institutions**: Automated question paper generation
2. **Online Learning Platforms**: Adaptive assessment systems
3. **Examination Boards**: Large-scale automated grading
4. **EdTech Companies**: Smart assessment tools

### Innovation & Impact

- **Time Savings**: Reduces question creation time by 70%
- **Consistency**: Maintains quality and difficulty standards
- **Scalability**: Can process thousands of answer sheets
- **Accessibility**: Makes quality assessments available to resource-limited institutions

### Technical Skills Demonstrated

- Natural Language Processing
- Question Generation algorithms
- Computer Vision (OpenCV)
- Image processing techniques
- OMR technology
- Python programming
- Algorithm design
- System integration

---

## Research Philosophy

My research work reflects my approach to problem-solving:

1. **Practical Focus**: Address real-world problems with measurable impact
2. **Interdisciplinary**: Combine multiple AI/ML techniques for robust solutions
3. **End-to-End Thinking**: From problem identification to deployment-ready systems
4. **Innovation**: Novel approaches backed by solid methodology

---

## Future Research Interests

While currently focused on industry applications, I maintain interest in:

- Multimodal AI systems
- Efficient fine-tuning of LLMs
- Evaluation metrics for generative AI
- AI safety and alignment
- Explainable AI in healthcare

---

## Publication Access

Both papers are available through academic databases. The full PDFs can be provided upon request, demonstrating:

- Research methodology
- Experimental design
- Results and analysis
- Code implementation details
- Future work directions

---

## Research Skills Summary

**Demonstrated Competencies:**

- Literature review and academic writing
- Experimental design and hypothesis testing
- Data collection and annotation
- Model development and evaluation
- Statistical analysis
- Technical communication
- Peer review process

**Tools & Technologies:**

- Python (TensorFlow, PyTorch, scikit-learn)
- NLP libraries (NLTK, spaCy, Transformers)
- OpenCV for computer vision
- LaTeX for academic writing
- Jupyter notebooks for experimentation

---

## Publication Links

## 1. To laugh or not to laugh – LSTM based humor detection approach

**Link**: https://ieeexplore.ieee.org/document/9580124

## 2. Generation and grading of arduous MCQs using NLP and OMR detection using OpenCV

**Link**: https://ieeexplore.ieee.org/document/9580089
