---
name: pdf-skill
description: PDFKit, PDF.js 및 Puppeteer와 같은 도구를 사용하여 PDF 문서를 생성, 구문 분석 및 조작하는 전문가입니다. PDF 작성, 콘텐츠 추출, 문서 병합 또는 양식 작성 시 사용합니다. 트리거에는 "PDF", "PDF 생성", "PDF 구문 분석", "PDF 추출", "PDF 병합", "PDF 양식", "PDFKit"이 포함됩니다.
---
# PDF 스킬

## 목적
프로그래밍 방식의 PDF 생성, 구문 분석 및 조작에 대한 전문 지식을 제공합니다. 처음부터 PDF 작성, 콘텐츠 추출, 문서 병합/분할, PDFKit, PDF.js, Puppeteer 및 유사한 도구를 사용한 양식 처리를 전문으로 합니다.

## 사용 시기
- 프로그래밍 방식으로 PDF 생성
- PDF에서 텍스트 또는 데이터 추출
- PDF 문서 병합 또는 분할
- 프로그래밍 방식으로 PDF 양식 채우기
- HTML을 PDF로 변환
- 워터마크 또는 주석 추가
- PDF 구조 및 메타데이터 구문 분석
- PDF 보고서 생성기 구축

## 빠른 시작
**다음과 같은 경우에 이 스킬을 호출하세요:**
- 코드 또는 데이터에서 PDF 생성
- PDF 파일에서 콘텐츠 추출
- PDF 병합, 분할 또는 조작
- PDF 양식 작성 또는 작성
- HTML/웹 페이지를 PDF로 변환

**다음과 같은 경우에는 호출하지 마세요.**
- Word 문서 작성 → `/docx-skill` 사용
- 엑셀/스프레드시트 작업 → `/xlsx-skill` 사용
- 파워포인트 작성 → `/pptx-skill` 사용
- 일반 파일 작업 → Bash 또는 파일 도구 사용

## 의사결정 프레임워크```
PDF Operation?
├── Generate from scratch
│   ├── Simple → PDFKit (Node) / ReportLab (Python)
│   └── Complex layouts → Puppeteer/Playwright + HTML
├── Parse/Extract
│   ├── Text extraction → pdf-parse / PyPDF2
│   └── Table extraction → Camelot / Tabula
├── Manipulate
│   └── pdf-lib (merge, split, edit)
└── Forms
    └── pdf-lib (fill) / PDFtk (advanced)
```

## 핵심 워크플로우

### 1. PDFKit을 이용한 PDF 생성
1. PDFKit(`npm install pdfkit`) 설치
2. 새 PDDocument 생성
3. 콘텐츠 추가(텍스트, 이미지, 그래픽)
4. 글꼴과 색상을 사용한 스타일
5. 필요에 따라 페이지를 추가하세요.
6. 파일 또는 응답으로의 파이프

### 2. HTML을 PDF로 변환
1. 인형사/극작가 설정
2. HTML 콘텐츠 또는 URL로 이동합니다.
3. 페이지 크기 및 여백 구성
4. 인쇄 옵션(머리글, 바닥글) 설정
5. PDF 버퍼 생성
6. 결과 저장 또는 스트리밍

### 3. PDF 구문 분석 및 추출
1. 파서 선택(pdf-parse, PyPDF2, pdfplumber)
2. PDF 파일 불러오기
3. 텍스트 또는 구조화된 데이터 추출
4. 여러 페이지로 구성된 문서 처리
5. 추출된 텍스트 정리 및 정규화
6. 원하는 형식으로 출력

## 모범 사례
- 가능하면 래스터 대신 벡터 그래픽을 사용하세요.
- 일관된 렌더링을 위해 글꼴 포함
- 다양한 리더에서 PDF 출력 테스트
- 스트리밍으로 대용량 PDF 처리
- 작업 복잡성에 적합한 라이브러리를 사용하십시오.
- 접근성 고려(태그된 PDF)

## 안티 패턴
| 안티 패턴 | 문제 | 올바른 접근 |
|---------------|---------|------|
| 이미지 전용 PDF | 검색/접근 불가 | 글꼴과 함께 텍스트 사용 |
| 글꼴 포함 없음 | 렌더링 문제 | 필수 글꼴 삽입 |
| 대용량 PDF를 로드하는 메모리 | 충돌 | 스트림 처리 |
| 암호화 무시 | 보안/액세스 문제 | 암호화된 PDF 처리 |
| 작업에 잘못된 도구 | 과도한 엔지니어링 | 도구를 복잡성에 맞추세요 |