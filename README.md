# Compiler Family Classifier
- 목적 : 
    - 여러 악성코드 식별 방법 중 Authorship Attribution 방법을 이용하여 악성코드를 식별 및 예방하려고 한다.
    - Authorship Attribution 방법을 이용하여 악성코드를 분류하기 위한 여러 특징들이 존재한다. 예를 들어, 코드 작성 스타일, 코드 문법, 컴파일러 정보 등이 있다.
    - 본 연구에서는 여러 특징 중에서 바이너리 코드(or 어셈블 코드)로부터 정적 분석을 통해 컴파일러 정보를 추출하는 것에 대해 서술하였다.
    - 특히, 컴파일러 정보 중 컴파일러 패밀리에 대한 정보를 추출하며, GCC, ICC, MSVC, XCODE 4개로 컴파일러를 분류하려고 한다.
--------------------------------------
- 선행 연구 기술 분석 : 
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
    - Ref : 
        - Rosenblum Nathan, Xiaojin Zhu, Barton Miller, "Learning to Analyze Binary Computer Code." AAAI. 2008.
        - Rosenblum Nathan, Barton Miller, Xiaojin Zhu, "Extracting Compiler Provenance from Program Binaries", Proceedings of the 9th ACM SIGPLAN-SIGSOFT workshop on Program analysis for software tools and engineering. ACM, 2010.
-------------------------------------
- 연구 프로젝트 목표 : 
    - "Assembly Code"로 부터 Instruction Code를 찾아 "Idiom 특징"을 가진 데이터 세트로 처리한다.
    - 선행 연구와 같이 Linear-chain CRF 모델을 이용하여 컴파일러를 분류한다.
    - 제안된 방법인 Genetic Compiler Feature List 방법을 통해 "Assembly Code"로 부터 특징을 추출한다.
    - Genetic Algorithm 모델을 정의하고 GCFL 특징을 통해 컴파일러를 분류한다.
------------------------------------- 
- 모델 설명 (지속적으로 추가 및 수정) : 
    - DataLoader Class : Assembly Code와 Hex Code를 통해 Idiom 특징 및 해당 hex 코드를 통합한 데이터 세트를 만든다.
    - MakeIdiomSet Class : Assembly Code에서 Instruction Code를 찾아 "Idiom 특징"을 가진 데이터 세트를 만든다.
    - CRFCompilerModel Class : 선행 연구와 동일한 방법으로 Linear-chain CRF 모델을 정의하고 Idiom 특징을 통해 컴파일러를 분류한다.
    - GACompilerProvenance : 추출된 Idiom 특징을 분석하여 입력 데이터(Assembly Code)들로부터 GCFL을 정의한다.
    - GAModel : Genetic Algorithm 을 통해 입력된 GCFL 데이터로부터 최적의 GCFL 특징을 정의한다.
-------------------------------------
- 실행 환경 : 
    - python : 3.6 이상
    - anaconda : 1.7.2 이상
    - os : windows 10 edu
    - IDE : pycharm
    - External library : 
        - sklearn_crfsuite : ver 0.4.0 (CRFCompilerModel 사용 시)
        - pandas : ver 0.24.2 이상
        - numpy : ver 1.16.2 이상
-------------------------------------
- 오픈소스화 : 
    - 해당 프로젝트는 컴파일러 분류 연구를 바탕으로 제작되었습니다.
    - 그러나 프로젝트 내에 내포된 linear-chain CRF, GA, GCFL, Idiom feature 등 다양한 모델 및 특징 추출 방법에 대한 클래스 및 기능들은 다양한 분야의 연구에 응용될 수 있습니다.
    - 제작된 라이브러리 자체적으로 사용하셔도 좋으나, 연구 및 활용에 따라 수정하셔서 사용하는 것을 추천합니다.
    - 해당 클래스를 사용하기 위한 다양한 기능, 연구 활용 방법에 대해서는 지속적으로 업데이트할 예정입니다.
    
## Version
* ### ver 0.0.1
    * DataLoader Class 정의
* ### ver 0.0.2
    * MakeIdiomSet Class 정의
* ### ver 0.0.3
    * CRFCompilerModel Class 정의
* ### ver 0.1.0    
    * GACompilerProvenance Class 정의
    * GAModel Class 정의
    * MakeIdiomSet Class 수정
        * 명령 수행 과정에 대한 print 문 주석 처리
    * Main.py 수정
        * CRF, GCFL 수행 과정에 대해 runCRFModel(), runGAModel() 로 구분
