# 프롬프트 템플릿

## 템플릿 라이브러리

### 코드 생성

**기본 코드:**
```python
template = "Write {language} code that {description}"
```
**제약조건 있음:**
```python
template = """
Write {language} code that {description}.

Requirements:
- Use {framework}
- Handle errors appropriately
- Include type hints
- Add documentation
"""
```
**코드 설명:**
```python
template = """
Explain the following {language} code:

```
{암호}
```

Focus on:
- Functionality
- Best practices
- Potential improvements
"""
```
### 텍스트 생성

**요약:**
```python
template = """
Summarize the following text in {max_sentences} sentences:

{text}
"""
```
**번역:**
```python
template = """
Translate the following text from {source_lang} to {target_lang}:

{text}
"""
```
**재작성:**
```python
template = """
Rewrite the following text in {tone} tone:

{text}
"""
```
### 질문 답변

**걸레 품질관리:**
```python
template = """
Based on the following context:

{context}

Answer the question: {question}

If the answer is not in the context, say "I don't know".
"""
```
**다단계 QA:**
```python
template = """
Step 1: {question1}
Step 2: Based on your answer, {question2}
Step 3: Finally, {question3}
"""
```
### 데이터 처리

**추출:**
```python
template = """
Extract the following information from the text:

Text: {text}

Extract:
- Names: {names}
- Dates: {dates}
- Locations: {locations}

Format as JSON.
"""
```
**분류:**
```python
template = """
Classify the following text into one of these categories:

Categories: {categories}

Text: {text}

Category:
"""
```
### 분석

**감정 분석:**
```python
template = """
Analyze the sentiment of the following text:

{text}

Provide:
- Overall sentiment (positive/negative/neutral)
- Confidence score (0-1)
- Key phrases influencing sentiment
"""
```
**주제 모델링:**
```python
template = """
Identify the main topics in the following text:

{text}

List topics with brief descriptions.
"""
```
## 신속한 엔지니어링 기술

### 생각의 사슬
```python
template = """
{question}

Think step by step:
1.
2.
3.
4.

Final answer:
"""
```
### 퓨샷 학습
```python
template = """
Examples:
Input: "I love this!"
Output: positive

Input: "This is terrible"
Output: negative

Input: "It's okay"
Output: neutral

Input: {input_text}
Output:
"""
```
### 자체 일관성
```python
template = """
Solve this problem: {problem}

Provide your reasoning and final answer.
"""
# Generate multiple responses, take majority vote
```
### 생각의 나무
```python
template = """
Problem: {problem}

Branch 1: {approach1}
Branch 2: {approach2}
Branch 3: {approach3}

Evaluate each branch and select the best solution.
"""
```
## 시스템 프롬프트

### 페르소나 정의
```python
system_prompt = """
You are an expert {domain} with {years} years of experience.
Your responses should be {tone} and include {level} of detail.
Always cite sources when applicable.
"""
```
### 작업 사양
```python
system_prompt = """
Your task is to {task_description}.

Constraints:
- {constraint1}
- {constraint2}
- {constraint3}

Output format: {format_specification}
"""
```
## 프롬프트 최적화

### A/B 테스트
```python
from prompt_engineer import PromptOptimizer

optimizer = PromptOptimizer()

template_a = "Summarize: {text}"
template_b = "Provide a concise summary of: {text}"

results = optimizer.compare_templates(
    [template_a, template_b],
    test_data=evaluation_set
)
```
### 반복적인 개선
```python
def improve_prompt(current_prompt, feedback):
    improved = llm.generate(f"""
    Improve this prompt based on feedback:

    Current prompt:
    {current_prompt}

    Feedback:
    {feedback}

    Improved prompt:
    """)

    return improved
```
## 모범 사례

1. **구체적으로**: 원하는 것을 명확하게 정의하세요.
2. **예제 사용**: 원하는 입력/출력 쌍 표시
3. **형식 지정**: 출력 구조를 명시적으로 정의합니다.
4. **제약조건 추가**: 응답 길이 또는 형식 제한
5. **철저한 테스트**: 다양한 입력을 검증합니다.
6. **버전 관리**: 시간 경과에 따른 프롬프트 변경 추적
7. **성능 모니터링**: 품질 지표 추적

## 일반적인 함정

1. **모호한 지침**: 일관되지 않은 출력으로 이어집니다.
2. **너무 복잡함**: 모델이 요구 사항을 놓칠 수 있음
3. **컨텍스트 누락**: 작업에 대한 정보가 부족함
4. **예시 없음**: 모델이 의도를 오해할 수 있음
5. **잘못된 형식**: 구조화된 출력을 구문 분석하기 어렵습니다.