
# Nome do Projeto - Modelo de IA

## Visão Geral

Este repositório contém um modelo de Inteligência Artificial treinado para a detecção de latas. O modelo foi treinado utilizando a técnica YOLO (You Only Look Once) e é capaz de identificar se as latas estão tombadas ou invertidas. Caso o número de latas detectadas em uma única operação exceda 10, o modelo envia um sinal por meio de um PLC (Controlador Lógico Programável) e registra essa ocorrência em um log detalhado, explicando os motivos da detecção.
<img src="https://github.com/VictorSilvaVS/VisionAlign/blob/main/testes/images/foto.teste.png" width=350>
## Funcionalidades

-  IA FEITA PARA DETECÇÃO DE LATAS INVERTIDAS OU TOMBADAS.
- CASO ELA DETECTE MAIS DE 10 OBJETOS TOMBADOS OU INVERTIDO, ELA EMITE UM SINAL BINÁRIO PARA PCL.
- ELA CONSEGUE DETECTAR FRATURA DE DOMO E EVITAR GERAÇÃO DE PERDAS CONSIDERÁVEIS.

## Tecnologias Usadas

- **Framework de IA**: O framework da IA é a ultralytics e YOLO (You Only Look Once)
- **Linguagem de Programação**: Python
- **Modelo Baseado em**: YOLO (You Only Look Once): Uma família de modelos de detecção de objetos em tempo real que analisam a imagem uma única vez (em vez de fazer múltiplas passagens) para identificar e classificar os objetos dentro dela.
- **Bibliotecas**:  cv2, queue,ultralytics  YOLO,multiprocessing,time

---

## Instalação

Siga os passos abaixo para instalar e executar o modelo a partir deste repositório.

### Pré-requisitos

1. **Python 3.10** deve estar instalado.
2. As dependências podem ser instaladas via `pip` ou `conda` (se você preferir ambientes isolados).

### Etapas de Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/VictorSilvaVS/VisionAlign.git
   cd VisionAlign
   ```

2. Crie e ative um ambiente virtual (opcional, mas recomendado):
   ```bash
   python -m venv env
   source env/bin/activate  # No Windows: env\Scripts\activate
   ```

3. Instale as dependências necessárias:
   ```bash
   pip install -r requirements.txt
   ```

   Se você estiver usando `conda`, pode instalar criando um ambiente baseado no arquivo de requisitos:
   ```bash
   conda create --name VisionAlign --file requirements.txt
   conda activate VisionAlign
   ```

---

## Como Usar

### Executando o Modelo

1. Certifique-se de que os dados necessários estão no formato correto. Para isso, use os arquivos de exemplo na pasta `data/` ou siga as instruções de formatação.

2. Para rodar o modelo, execute o seguinte script:

   ```bash
   python script_principal.py --input "caminho/para/dados"
   ```

   Isso carregará o modelo treinado e processará os dados de entrada. O resultado será salvo no diretório `output/`.

### Exemplos de Uso

Aqui estão alguns exemplos de como rodar o modelo:

- Para processar um único arquivo de imagem:
  ```bash
  python script_principal.py --input "data/imagem.jpg"
  ```

- Para processar um conjunto de dados:
  ```bash
  python script_principal.py --input "model/dataset/"
  ```

### Ajustando Hiperparâmetros

Se você quiser ajustar os hiperparâmetros do modelo, como taxa de aprendizado, número de camadas, ou tamanho de lote, edite o arquivo `config.json` ou passe os parâmetros diretamente na linha de comando.

---

## Estrutura do Projeto

- **model/**: Contém o arquivo do modelo pré-treinado.
- **data/**: Contém exemplos de dados de entrada e saída.
- **src/**: Código-fonte do projeto.
- **output/**: Resultados gerados pela IA.
- **config.json**: Arquivo de configuração para ajustar parâmetros do modelo.
- **requirements.txt**: Dependências do projeto.
- **main.py**: Script principal para rodar a IA.

---

## Contribuição

Se você deseja contribuir para o desenvolvimento do projeto, siga os passos abaixo:

1. Faça um fork do repositório.
2. Crie um branch com a nova funcionalidade (`git checkout -b minha-nova-funcionalidade`).
3. Faça commit das suas mudanças (`git commit -am 'Adicionei nova funcionalidade'`).
4. Envie o código para o branch (`git push origin minha-nova-funcionalidade`).
5. Abra um Pull Request.

---

## Licença

Este projeto está licenciado sob a [APACHE,  Version 2.0 ]. Consulte o arquivo [LICENSE](LICENSE) para mais informações.

---

## Contato

Para questões ou sugestões, entre em contato pelo grupo do discord: [https://discord.gg/Haw9RbNS]
