# Fluxo 4: Cadastrar Atividade da Tarefa (PAT)

## 📖 Glossário de Vínculos
| Entidade | Referência | Descrição |
| :--- | :--- | :--- |
| **idTarefa** | Fluxo Anterior | ID da tarefa gerada no fluxo "Atribuir Tarefa". |
| **Data PAT** | Contexto | Data de início registrada no PAT original. |
| **idDemandaPat** | Fluxo 2 | Vínculo hierárquico entre a Demanda e o PAT. |

---

## 🛠 Especificação Técnica: Cadastrar Atividade
**Documentação** `http://pats.sigep.docker.localhost/docs/api#/`
**Url** `http://pats.sigep.docker.localhost`
**Ação:** `POST /api/pats/atividades/store`

### Regras de Validação e Lógica de Registro
Este fluxo registra o esforço técnico despendido em uma tarefa específica.

| Campo | Regra de Validação | Lógica de Geração (Mock/Faker) |
| :--- | :--- | :--- |
| `idTarefa` | `required|int` | **Obrigatório.** ID retornado no fluxo de Atribuição. |
| `descricaoAtividade` | `required|string` | Texto descritivo de **100 caracteres** (Faker). |
| `tempoCorrido` | `required|numeric` | Valor aleatório entre **1 e 10**. |
| `dataInicio` | `required|date_format:d/m/Y H:i:s` | **Data de Início do PAT vinculado**. |
| `dataTermino` | `required|date_format:d/m/Y H:i:s` | **Mesma data** informada em `dataInicio`. |
| `deslocamento` | `required|string|in:S,N` | Valor fixo: **'N'**. |
| `cidade` | `nullable|string` | Valor padrão: `null`. |

---

## 🔄 Fluxo Lógico para o Agente de IA (Antigravity)

1. **Recuperação de Cronologia:** O agente deve buscar a data de criação do PAT (Fluxo 1) para preencher os campos `dataInicio` e `dataTermino`, garantindo que a atividade não tenha data retroativa ou futura inconsistente.
2. **Cálculo de Esforço:** O `tempoCorrido` deve ser tratado como um valor numérico que representa o tempo investido na atividade.
3. **Consistência de Localização:** Como o `deslocamento` é sempre 'N', o campo `cidade` deve obrigatoriamente ser enviado como `null` ou ignorado, conforme a regra de negócio.

---

## 📂 Exemplo de Payload JSON
```json
{
  "idTarefa": 5566,
  "descricaoAtividade": "Realizada a configuração do ambiente de desenvolvimento e deploy dos primeiros containers Docker.",
  "tempoCorrido": 4.5,
  "dataInicio": "17/03/2026 09:00:00",
  "dataTermino": "17/03/2026 09:00:00",
  "deslocamento": "N",
  "cidade": null
}