# Follow-Up Desktop App

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![PySide6](https://img.shields.io/badge/PySide6-Qt%20for%20Python-orange?style=for-the-badge&logo=qt)
![SQLite](https://img.shields.io/badge/SQLite-3-darkblue?style=for-the-badge&logo=sqlite)
![Status](https://img.shields.io/badge/Status-Concluído-green?style=for-the-badge)

Sistema de desktop para gerenciamento e acompanhamento de atividades (follow-ups), desenvolvido com foco em robustez, usabilidade e manutenibilidade.

A aplicação foi projetada para oferecer uma solução local e eficiente para controle de registros, implementando um sistema de **CRUD** completo com persistência de dados em um banco de dados relacional **SQLite**. A interface gráfica construída, foi pensada para ser intuitiva, facilitando o uso por usuários não técnicos. O objetivo deste projeto


![Gif da Aplicação](demo.gif)

---

## 🎯 Funcionalidades Principais

* **Interface Gráfica Intuitiva:** UI limpa e objetiva, desenvolvida com PySide6 (Qt for Python), focada na experiência do usuário.
* **Operações CRUD Completas:** Implementação de todas as operações essenciais de manipulação de dados:
    * **C**reate (Criar): Adição de novos registros de follow-up.
    * **R**ead (Ler): Visualização e busca de registros existentes.
    * **U**pdate (Atualizar): Edição de informações dos registros.
    * **D**elete (Deletar): Exclusão de registros.
* **Persistência de Dados Confiável:** Utiliza um banco de dados relacional (SQLite) para garantir a integridade e a consistência dos dados, aderindo a princípios transacionais (**ACID** - Atomicidade, Consistência, Isolamento e Durabilidade).
* **Exportação de Dados:** Funcionalidade para exportar a base de dados completa, permitindo a extração de dados para backups ou análises externas (um processo análogo a uma operação de **ETL** - Extract, Transform, Load).
* **Instalador Simplificado:** Um instalador executável (`.exe`), criado com Inno Setup, que automatiza o processo de instalação e configuração do ambiente para o usuário final.

---

## 📖 Contexto do Projeto  

Centros de ensino frequentemente dependem de planilhas para gerenciar contatos e follow-ups, o que leva a desafios como dados descentralizados, risco de erros manuais e grande dificuldade para extrair informações estratégicas de forma rápida.

Esta aplicação desktop surgiu como uma solução real completa para eliminar esses gargalos em uma unidade Fisk Centro de Ensino. Através de uma interface intuitiva e de fácil instalação. O sistema oferece:

- Centralização de todos os cadastros e interações em um banco de dados relacional, garantindo a integridade, segurança e padronização dos dados.

- Eficiência operacional, permitindo que a equipe realize buscas, atualizações e exportações de dados em alguns segundos e com poucos cliques, ao invés de horas em um ambiente confuso ou com ferramentas descentralizadas e pouco eficiêntes para follow-up, como planilhas e follow-up físico.

- Conversão de dados brutos em insights através de um módulo de visualização com filtros personalizados e um dashboard com gráficos focados nos principais indicadores de desempenho (KPIs), facilitando a tomada de decisões e extração de insights. 

---

### ✨ Funcionalidades

* **Gestão de Contatos (CRUD):**
    * Cadastro, edição e exclusão de contatos com formulário detalhado.
    * Ordenação de dados instantânea ao clicar nos cabeçalhos das colunas (ex: por Nome, Data da Visita, Status).

* **Sistema de Filtragem Avançada:**
    * Busca por nome parcial e por qualquer sequência de dígitos do telefone.
    * Filtros combináveis por Atendente, Curso de Interesse, Status e Período de Visita.

* **Dashboard de Business Intelligence (BI):**
    * Módulo de relatórios com visualizações gráficas para análise de performance.
    * Gráficos de análise de funil (Visitas vs. Matrículas).
    * Distribuição de leads por status.
    * Análise de eficácia dos canais de aquisição ("Como conheceu").
    * Identificação dos cursos com maior demanda.

* **Utilitários de Dados:**
    * **Entrada de Dados Assistida:** Autoformatação em tempo real para datas (`ddmmyyyy` → `dd/mm/yyyy`), telefones e valores monetários.
    * **Exportação para CSV:** Geração de relatórios `.csv` que respeitam a filtragem e ordenação aplicadas na tela.
    * **Detecção de Duplicados:** Ferramenta para identificar contatos com telefone ou e-mail duplicados, visando a integridade da base.
    * **Backup e Portabilidade:** Funcionalidade de backup do banco de dados SQLite com um clique, gerando um arquivo com timestamp.

* **Arquitetura e Distribuição:**
    * **Interface Responsiva:** UI construída com `ttkbootstrap`, garantindo uma experiência de usuário moderna e funcional.
    * **Banco de Dados Embarcado:** Utilização de SQLite 3 para uma solução `zero-config`, onde o banco é um arquivo local.
    * **Instalador para Windows:** O projeto é distribuído como um pacote completo com um instalador (`setup.exe`) criado com Inno Setup.
    * **Integração com SO:** Definição de `AppUserModelID` via `ctypes` para garantir a correta identidade visual (ícone) na barra de tarefas do Windows.

---

### 🔑 Funcionalidades Principais

**Pipeline de Gerenciamento de Leads (CRM):**
A aplicação implementa um ciclo de vida completo de gerenciamento de contatos, desde a prospecção até a conversão. As operações de CRUD são centralizadas em uma interface intuitiva, permitindo que a equipe comercial mantenha um registro detalhado e atualizado de cada lead.

**Módulo de Business Intelligence (BI) e Analytics:**
O diferencial do projeto é seu dashboard analítico, que transforma dados operacionais em insights estratégicos. Através de um pipeline de ETL in-memory (SQLite → Pandas → Matplotlib), a ferramenta visualiza KPIs essenciais:
* **Taxa de Conversão:** Acompanhamento da eficácia do funil de vendas (Visitas vs. Matrículas).
* **Análise de Canais:** Identificação dos canais de aquisição mais eficientes (ex: Indicação, Mídias Sociais), permitindo a otimização de investimentos em marketing.
* **Saúde do Pipeline:** Visão clara da distribuição de leads por status, ajudando a prever resultados e identificar gargalos no processo de negociação.

**Utilitários de Qualidade e Integridade de Dados:**
Para garantir a confiabilidade das análises, a aplicação possui ferramentas focadas na qualidade dos dados:
* **Normalização na Entrada:** A autoformatação de telefones, datas e valores monetários não só agiliza o cadastro, mas também padroniza os dados na origem, mitigando erros de digitação e garantindo a consistência para futuras consultas.
* **Detecção de Duplicados e Backup:** Ferramentas essenciais que permitem a limpeza da base de dados e a recuperação de desastres, assegurando que o ativo mais importante — os dados dos contatos — esteja sempre seguro e íntegro.

**Deployment Zero-Config (SQLite + Inno Setup):**
A escolha pelo SQLite como banco de dados embarcado elimina a necessidade de qualquer configuração de servidor. Combinado com um instalador profissional criado com Inno Setup, a distribuição e o setup da aplicação em um novo computador são processos triviais, podendo ser realizados em segundos por qualquer usuário.

---

### 📊 Impacto e Valor de Negócio

A implementação desta ferramenta representa a transição de um modelo de gestão reativo e manual para uma **cultura proativa e orientada a dados (Data-Driven)**.

* **Eficiência Operacional:** A centralização dos dados e os filtros dinâmicos reduzem drasticamente o tempo gasto para encontrar um contato ou segmentar uma lista para uma campanha de follow-up. A autoformatação minimiza erros de digitação e retrabalho.

* **Tomada de Decisão Estratégica:** O dashboard de BI fornece aos gestores uma visão clara e objetiva da performance comercial. Perguntas como "Qual canal de marketing está trazendo mais matrículas?" ou "Qual curso está com maior procura este mês?" são respondidas com dados, não com suposições.

* **Aumento de Conversão:** Ao garantir um processo de follow-up mais organizado e permitir a identificação de leads "esquecidos", a ferramenta atua diretamente na mitigação da perda de oportunidades, com impacto direto no **aumento da taxa de matrículas**.

---

## 🛠️ Arquitetura e Conceitos Técnicos

Este projeto foi além da simples implementação de funcionalidades, incorporando boas práticas de desenvolvimento para garantir um software robusto de qualidade.

* **Banco de Dados Relacional (SQLite):** A escolha pelo SQLite como SGBD se deu pela sua simplicidade, portabilidade e eficiência em aplicações desktop. O banco de dados armazena os dados de forma estruturada, permitindo consultas complexas e garantindo a integridade referencial dos dados.

* **Camada de Persistência de Dados:** Toda a interação com o banco de dados é centralizada em um módulo dedicado (`database.py`), abstraindo a lógica de SQL do restante da aplicação. Essa separação de responsabilidades torna o código mais limpo, seguro, e facilita futuras migrações de banco, se necessário.

* **Modularização e Manutenibilidade:** O código é estruturado de forma modular, separando as responsabilidades:
    1.  **Interface do Usuário (UI):** Arquivos e classes Python que gerenciam a lógica da interface.
    2.  **Lógica de Negócio:** Funções que orquestram as operações e regras da aplicação.
    3.  **Acesso aos Dados:** A camada de persistência que lida exclusivamente com o banco de dados.

    Essa abordagem facilita a manutenção, a escalabilidade e a implementação de novos recursos sem impactar outras partes do sistema.

---

## 🚀 Tecnologias Utilizadas

| Tecnologia | Finalidade |
| :--- | :--- |
| **Python** | Linguagem principal do projeto |
| **SQLite3** | Banco de dados relacional embarcado para persistência de dados |
| **Inno Setup** | Ferramenta para criação do instalador para Windows |

---

## 🖼️ Screenshots da Aplicação

| Tela Principal | Tela de Cadastro/Edição |
| :---: | :---: |
| ![Tela de Cadastro e Acompanhmento](images/interface_cadastro_acompanhamento.png) | ![Tela de Relatórios](images/interface_relatórios.png) |

---

## ⚙️ Instalação e Execução

Existem três formas de utilizar a aplicação: através do instalador, através do download direto da pasta raiz ou executando o código-fonte diretamente.

### Para Usuários Finais

1.  Acesse a pasta no Google Drive [**Releases**](https://drive.google.com/drive/folders/1r2k4mYVWIGz0aybD9Z9T5ToEFVC813Le?usp=sharing).
2.  Baixe o instalador `setup-follow-up-app.exe` ou o `Fisk FollowUp.zip` para fazer o dowload diretamente da pasta com o executável.
3.  Como utilizar:
      - Caso escolha baixar o `setup-follow-up-app.exe`, execute o instalador e siga as instruções na tela.
      - Caso escolha baixar o `Fisk FollowUp.zip`, basta extrair o conteúdo e executar diretamente o `Fisk FollowUp.exe` que está dentro da pasta raiz.
- **Recomendação:** Utilizar o `setup-follow-up-app.exe`. É a forma mais simples e rápida, uma vez que é tudo feito automaticamente pelo instalador.

### Para Desenvolvedores

**Pré-requisitos:**
* Python 3.10 ou superior
* Git

**Passo a passo:**
```bash
# 1. Clone o repositório
git clone [https://github.com/gustavochotti/follow-up-desktop-app.git](https://github.com/gustavochotti/follow-up-desktop-app.git)

# 2. Acesse o diretório do projeto
cd follow-up-desktop-app

# 3. Crie e ative um ambiente virtual (recomendado)
python -m venv .venv
# No Windows:
.\.venv\Scripts\activate
# No Linux/macOS:
source .venv/bin/activate

# 4. Instale as dependências
pip install -r requirements.txt

# 5. Execute a aplicação
python main.py
```

---

## ⚠️ Informações Importantes

Antes de utilizar a aplicação, por favor, leia os pontos abaixo para entender como ela funciona e como garantir a segurança dos seus dados.

* **Armazenamento de Dados Local:** Todo o banco de dados da aplicação é armazenado em um único arquivo chamado `contacts.db`. Este arquivo é criado no mesmo diretório onde o programa foi instalado. Isso significa que **todos os seus dados residem exclusivamente no seu computador**, garantindo total privacidade.

* **Backups e Restauração de Dados:** Como os dados são locais, **a responsabilidade de realizar backups é do usuário**. Para evitar perdas acidentais de informação, recomendamos fortemente as seguintes práticas:
    * **Para fazer um backup:** Utilize a funcionalidade de "Exportar Banco de Dados" dentro da aplicação ou copie manualmente o arquivo `contacts.db` para um local seguro (um HD externo, um serviço de nuvem, etc.).
    * **Para restaurar um backup:**
        1.  **Feche a aplicação** completamente.
        2.  Pegue o seu arquivo de backup e renomeie-o para `contacts.db`.
        3.  Encontre a pasta onde o programa foi instalado. **Dica:** se você não sabe o local, clique com o botão direito no atalho do programa na sua Área de Trabalho e selecione a opção "Abrir local do arquivo".
        4.  Mova ou copie o seu backup (`contacts.db`) para dentro dessa pasta, **substituindo** o arquivo antigo quando solicitado.
        5.  Abra a aplicação novamente. Seus dados restaurados estarão lá.

* **Aplicação Monousuário (Standalone):** O sistema foi projetado para ser utilizado **sem a necessidade de um login**. Ele não possui funcionalidades de rede ou sincronização. Se você instalar a aplicação em outra máquina, ela terá um banco de dados separado e vazio. No entanto, é possível **transferir seus dados para outro computador manualmente**. Para isso, siga **exatamente o mesmo procedimento descrito acima em "Para restaurar um backup"**: copie o arquivo `contacts.db` do computador antigo e use-o para substituir o arquivo original na pasta raiz do projeto da nova instalação.

* **Compatibilidade do Instalador:** O instalador (`.exe`) fornecido foi criado e testado exclusivamente para o ambiente **Windows (versões 10 e 11)**. Embora o código-fonte seja multiplataforma, a versão pronta para uso é destinada a usuários do Windows.

---

## 📊 Potencial para Aplicações Analíticas

- **Pipeline de ETL:** A extração do banco de dados pode ser o ponto de partida para um pipeline de ETL, onde os dados seriam transformados e carregados em um data warehouse ou data lake para análises consolidadas.
- **Análise de Dados:** Os dados podem ser utilizados para gerar dashboards em ferramentas como Power BI ou Tableau, ou analisados com bibliotecas Python (Pandas, Matplotlib, Seaborn) para responder a perguntas de negócio, como:
  - Qual a frequência de follow-ups por categoria?
  - Qual o tempo médio para conclusão de uma atividade?
  - Existem padrões ou sazonalidades nos registros?
- **Machine Learning:** Em uma escala maior, o histórico de dados poderia ser usado para treinar modelos preditivos, como prever a probabilidade de atraso em determinadas tarefas ou identificar anomalias nos registros.

---

## 👨‍💻 Autor
**Gustavo Chotti** 

[**Github**](https://github.com/gustavochott) | [**LinkedIn**](https://www.linkedin.com/in/gustavochotti)

---

## 📄 Licença
Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.
