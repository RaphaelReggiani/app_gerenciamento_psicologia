# Sistema de Gerenciamento de Pacientes em Psicologia

Aplicação desenvolvida com **Python** e **Django**, utilizando **HTML** e **CSS**, pronta para deploy, voltado para a área de psicologia. O sistema permite o controle e o acompanhamento de pacientes por parte dos psicólogos(as).

## 🔧 Funcionalidades

- Cadastro de usuários para os psicólogos(as) (ativação através de e-mail enviado ao endereço de e-mail corporativo do psicólogo(a), hashing de senha e as devidas validações);
- Edição de dados do perfil dos psicólogos(as) cadastrados;
- Cadastro de pacientes (necessário estar logado, sendo um psicólogo(a));
- Gerenciamento de pacientes (apenas logado e sendo necessário ser o psicólogo(a) que cadastrou / responsável pelo paciente);
- Página com todos os pacientes de cada psicólogo(a), incluindo filtros de pesquisa;
- Registro detalhado de consultas (permitido ser realizado apenas pelo psicólogo(a) responsável pelo paciente em questão), incluindo gráfico de humor e resumo com link direto para as últimas consultas;
- Histórico de consultas com destaque visual por humor (vermelho, amarelo e branco), com link direto para os dados registrados da consulta;
- Visualização das informações das consultadas registradas;
- Banco de dados usando MySQL.

OBS: Os acessos aos pacientes, são restritos para o psicólogo responsável pelos mesmos, não acessível a outros psicólogos.

## Imagens da Aplicação

### Página Inicial - Sem Log in
![Home Page - Sem estar logado](readme_assets/home_page_sem_login.png)

### Página Inicial - Logado 
![Home Page - Logado](readme_assets/home_page_logado.png)

### Página de Cadastro / Log in
![Cadastro / Log in](readme_assets/cadastro_login_page.png)

### Cadastro de Pacientes - Sem Log in
![Cadastro de Pacientes - Erro (Sem usuário logado)](readme_assets/cadastro_erro_sem_login.png)

### Cadastro de Pacientes - Logado
![Cadastro de Pacientes - Logado](readme_assets/cadastro_paciente_logado.png)

### Registro de Consulta (Parte 1) - Apenas com usuário logado e responsável pelo paciente em questão
![Registro de Consulta - Parte 1](readme_assets/registro_consulta_logado_1.png)

### Registro de Consulta (Parte 2) - Apenas com usuário logado e responsável pelo paciente em questão
![Registro de Consulta - Parte 2](readme_assets/registro_consulta_logado_2.png)

### Registro de Consulta (Gráfico) - Apenas com usuário logado e responsável pelo paciente em questão
![Registro de Consulta - Gráfico](readme_assets/registro_consulta_logado_grafico.png)

### Consulta Registrada  - Apenas com usuário logado e responsável pelo paciente em questão
![Consulta Registrada](readme_assets/consulta.png)

### Página de pacientes do psicólogo(a)  - Apenas com usuário logado e responsável pelo paciente em questão
![Página de pacientes](readme_assets/pacientes_psicologo_page.png)

### Edição dos dados do usuário psicólogo(a)
![Edição de dados de usuário psicólogo(a)](readme_assets/edicao_psicologo.png)

### Edição dos dados do paciente - Apenas com usuário logado e responsável pelo paciente em questão
![Edição de dados do paciente](readme_assets/atualizar_dados_paciente.png)

