# Compiler Family Classifier
- 목적 : 
    - 여러 악성코드 식별 방법 중 Authorship Attribution 방법을 이용하여 악성코드를 식별 및 예방하려고 한다.
    - Authorship Attribution 방법을 이용하여 악성코드를 분류하기 위한 여러 특징들이 존재한다. 예를 들어, 코드 작성 스타일, 코드 문법, 컴파일러 정보 등이 있다.
    - 본 연구에서는 여러 특징 중에서 바이너리 코드로부터 정적 분석을 통해 컴파일러 정보를 추출하는 것에 대해 서술하였다.
    - 특히, 컴파일러 정보 중 컴파일러 패밀리에 대한 정보를 추출하며, GCC, ICC, MSVC, XCODE 4개로 컴파일러를 분류하려고 한다.
- 기술 : 
    - Main Idea : 
        - Function Entry Point 를 찾는다.
        - FEP를 비교한다.
        - 패턴을 분석한다.
        - 분석된 내용을 기반으로 Compiler Family 를 구별한다. 
    - Context 기반 : Idiom + wildcard + n-gram(size : 3)
    - Structure 기반(Negative Value) : 
        - Call-Consistency Feature : Entry 안에 'Call'이 포함된 여부
        - Binary Overlap Feature : Entry 안에 기존 바이트코드와 비슷한 코드가 있는지 여부
    - Model : 
        - Conditional Random Field : 연속적인 입력에 대한 연속적인 분류 추론 방법
- 연구 아이디어 : 
    - GA 를 사용하여 컴파일러 패밀리 별 유전 특징을 추출한다.
    - 추출된 유전 특징을 이용하여 학습된 내용들을 보여줄 수 있다. (이미지로 보여줄 예정, 0, 1, 2, Code 별 색)
    - 학습된 히스토리를 보여줄 수 있다.

## Version
* ### ver 0.0.1
    * DataLoader Class
* ### ver 0.0.2
    * MakeIdiomSet Class
* ### ver 0.0.3
    * CRFCompilerModel Class
