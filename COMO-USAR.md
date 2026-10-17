# Seu novo perfil

Este pacote está preparado para o repositório **ValterVS/ValterVS**, que já existe. Faça uma cópia do README atual antes de substituir os arquivos.

1. Coloque os arquivos deste pacote na raiz do repositório, incluindo a pasta oculta `.github`.
2. Faça commit na branch principal. O cartão já funciona com os dados incluídos.
3. Na aba **Actions**, habilite os workflows se o GitHub solicitar. Execute **Atualizar perfil → Run workflow** para conferir a atualização.
4. Se houver erro de permissão no envio, em **Settings → Actions → General → Workflow permissions**, permita leitura e escrita. Regras de proteção da branch também podem impedir commits do workflow.

O workflow consulta apenas dados públicos e usa o `GITHUB_TOKEN` automático, sem token pessoal. Atualiza diariamente às 09:17 UTC (06:17 em Brasília); o GitHub pode atrasar execuções agendadas.

## Personalização

Edite `profile.json` para mudar textos, tecnologias e contatos. Os dados editoriais vieram da bio e do README público de ValterVS; a bio descreve estudante de Engenharia de Software e desenvolvedor Java Jr., enquanto o README enfatiza full stack e IA/ML. O cartão evita afirmar senioridade e mantém as áreas declaradas no perfil. Atualize os destaques no README quando desejar.

O retrato foi convertido diretamente da foto fornecida em caracteres coloridos, armazenados em `assets/portrait.json`. A foto original não é distribuída. Não há geração de rosto por IA nem cópia do retrato de Andrew.

As métricas são repositórios públicos (incluindo forks), seguidores e estrelas dos repositórios próprios (excluindo forks). Não são estimados commits ou linhas de código. A data representa a última consulta bem-sucedida, em UTC. As linguagens principais por repositório também são guardadas em `assets/stats.json`; a lista de stack é editorial, conforme o README de origem.

Para gerar localmente com Python 3.10 ou superior, sem dependências:

```sh
python scripts/update_profile.py
python scripts/update_profile.py --offline
```

Os SVGs não carregam imagens externas. Links dentro de SVGs podem não ser clicáveis no GitHub; por isso os contatos também estão no README.

## Referências

- Conceito visual: https://github.com/Andrew6rant/Andrew6rant
- Bio e dados: https://api.github.com/users/ValterVS
- Textos e stack: https://github.com/ValterVS/ValterVS
- Projetos: https://api.github.com/users/ValterVS/repos

Implementação original: nenhum código do repositório de referência foi reutilizado.
