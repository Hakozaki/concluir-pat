# Fluxo 3: Atribuição de Tarefa a uma demanda de um PAT (Pedido de Apoio Técnico)

## 📖 Glossário de Apoio
| Entidade | Valor / Regra | Descrição |
| :--- | :--- | :--- |
| **idDemandaPat** | Referência Externa | ID gerado no fluxo "Demandar PAT". |
| **Usuários** | 2 (Marcus), 114 (Edelmar) | Técnicos responsáveis. |
| **Setores** | 1488 (Sistemas), 1059 (T.I) | Setores vinculados aos usuários. |

---

## 🛠 Especificação Técnica: Atribuir Tarefa
**Documentação** `http://pats.sigep.docker.localhost/docs/api#/`
**Url** `http://pats.sigep.docker.localhost`
**Ação:** `POST /api/pats/tarefas/store`

### Campos e Regras de Negócio
O payload deve ser construído respeitando a integridade entre o setor e o técnico atribuído.

| Campo | Regra de Validação | Lógica de Geração (Mock/Faker) |
| :--- | :--- | :--- |
| `idDemandaPat` | `required|int` | Deve ser o ID retornado na vinculação anterior. |
| `descricaoTarefa` | `required|string|min:20` | Texto técnico aleatório de **50 caracteres**. |
| `prazoTarefa` | `date(d/m/Y)\|nullable` | **Data do PAT original + 10 dias**. |
| `idsUsuariosAtribuidos`| `required|array` | **Lógica de Setor:** <br>• Se Setor = 1488, usar `[2]` <br>• Se Setor = 1059, usar `[114]` |

---

## 🔄 Fluxo Lógico para o Agente de IA (Antigravity)

1. **Vínculo de Operação:** O agente deve localizar o `idDemandaPat` correto para garantir que a tarefa seja atribuída à demanda certa.
2. **Inteligência de Atribuição:** Antes de preencher `idsUsuariosAtribuidos`, o agente deve validar qual setor foi definido no fluxo anterior. 
   - O usuário **Marcus (2)** nunca deve receber tarefas do setor **1059**.
   - O usuário **Edelmar (114)** nunca deve receber tarefas do setor **1488**.
3. **Formatação de Data:** Garantir que o `prazoTarefa` siga o padrão brasileiro `dia/mês/ano`.

---

## 📂 Exemplo de Payload JSON (Setor Sistemas)
```json
{
  "idDemandaPat": 987,
  "descricaoTarefa": "Desenvolver os endpoints de integração com o banco NAT.",
  "prazoTarefa": "27/03/2026",
  "idsUsuariosAtribuidos": [2]
}