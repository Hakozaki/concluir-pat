# Fluxo 1: Criação do PAT (Pedido de Apoio Técnico)

## 📖 Glossário de Domínio (Entidades e IDs)
| Termo | Valor/ID | Descrição |
| :--- | :--- | :--- |
| **Entidade NAT** | 2 | Entidade principal do fluxo. |
| **Usuários Disponíveis** | 2 (Marcus), 76 (Wldilene), 114 (Edelmar) | IDs permitidos para `idProprietario`. |
| **Setores** | 1488 (Sistemas), 1059 (T.I) | IDs permitidos para `idSetor`. |
| **Prioridades** | 3 (Normal), 4 (Baixa) | Níveis de urgência. |

---

## 🛠 Especificação Técnica do Endpoint
**Documentação** `http://pats.sigep.docker.localhost/docs/api#/`
**Url** `http://pats.sigep.docker.localhost`
**Ação:** `POST /api/pats/store`

### Regras de Validação e Mock de Dados
O fluxo deve seguir rigorosamente as regras abaixo para a criação do registro:

| Campo | Regra de Validação | Lógica de Geração (Faker/Mock) |
| :--- | :--- | :--- |
| `idEntidade` | `required|int` | ID da entidade de contexto. |
| `idEntidadeSolicitante` | `required|int` | **Sempre 2**. |
| `idProprietario` | `required|int` | Aleatório entre: `[2, 76, 114]`. |
| `idSetor` | `required|int` | Aleatório entre: `[1488, 1059]`. |
| `prioridade` | `required|int` | Aleatório entre: `[3, 4]`. |
| `tipoProcesso` | `required|string` | **Sempre 'pedidoInterno'**. |
| `numeroReferencia` | `nullable|string` | `null`. |
| `numeroProcesso` | `nullable|string` | `null`. |
| `descricaoPat` | `required|string` | Texto aleatório de **500 caracteres**. |
| `prazoPat` | `date(d/m/Y)|nullable` | Data atual + **Random(10 a 20 dias)**. |
| `justificativaPrioridade`| `nullable` | `null`. |
| `expectativaResposta` | `date(d/m/Y)|nullable` | Mesma data gerada para `prazoPat`. |
| `idsQuesito` | `array|nullable` | `null`. |

---

## 🔄 Fluxo Lógico para o Agente de IA

1. **Cálculo de Datas:** Obter a data atual, somar entre 10 e 20 dias para o `prazoPat` e replicar em `expectativaResposta` no formato `d/m/Y`.
2. **Geração de Conteúdo:** A `descricaoPat` deve ser um texto rico (lorem ipsum ou técnico) com exatamente ou mais de 500 caracteres.
3. **Mapeamento de IDs:** Utilizar apenas os IDs fornecidos no glossário para garantir a integridade referencial do mock.

---

## 📂 Exemplo de Payload JSON
```json
{
  "idEntidade": 2,
  "idEntidadeSolicitante": 2,
  "idProprietario": 114,
  "idSetor": 1059,
  "prioridade": 4,
  "tipoProcesso": "pedidoInterno",
  "numeroReferencia": null,
  "numeroProcesso": null,
  "descricaoPat": "[Texto de 500 caracteres aqui...]", 
  "prazoPat": "30/03/2026",
  "justificativaPrioridade": null,
  "expectativaResposta": "30/03/2026",
  "idsQuesito": null
}
