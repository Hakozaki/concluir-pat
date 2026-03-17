# Fluxo 2: Atribuir Demanda a um PAT (Pedido de Apoio Técnico)

## 📖 Glossário de Demandas e Setores
| Entidade | ID | Descrição |
| :--- | :--- | :--- |
| **Demanda** | 10009 | PESQUISA NOS BANCOS DE DADOS |
| **Demanda** | 10030 | SUPORTE TÉCNICO - T.I. |
| **Demanda** | 30170 | ELABORAÇÃO DE SOLUÇÃO EM TI (SISTEMAS) |
| **Setor** | 1488 | NAT - COORDENAÇÃO DE DESENVOLVIMENTO DE SISTEMAS |
| **Setor** | 1059 | NAT - COORDENAÇÃO DE TECNOLOGIA DA INFORMAÇÃO |

---

## 🛠 Especificação Técnica: Demandar PAT
**Documentação** `http://pats.sigep.docker.localhost/docs/api#/`
**Url** `http://pats.sigep.docker.localhost`
**Ação:** `POST /api/pats/demandas/store`

### Regras de Validação e Lógica de Dados
Este fluxo associa uma demanda específica a um PAT já existente.

| Campo | Regra de Validação | Lógica de Geração (Mock/Input) |
| :--- | :--- | :--- |
| `idPat` | `required|int` | **Obrigatório.** Deve ser o ID do PAT criado no fluxo anterior. |
| `idDemanda` | `int|nullable` | Se não fornecido, escolher aleatório: `[10009, 10030, 30170]`. |
| `idSetor` | `required|int` | Aleatório entre: `[1488, 1059]`. |
| `despacho` | `string|nullable` | Valor padrão: `null`. |

---

## 🔄 Fluxo Lógico para o Agente de IA

1. **Verificação de Dependência:** O agente deve garantir que possui um `idPat` válido antes de executar este fluxo.
2. **Seleção de Especialidade:** Caso a `idDemanda` não seja especificada no prompt de execução, o agente deve selecionar uma das três opções do glossário de forma equilibrada.
3. **Atribuição de Setor:** O `idSetor` deve ser obrigatoriamente um dos IDs do NAT (Sistemas ou T.I) listados acima.

---

## 📂 Exemplo de Payload JSON
```json
{
  "idPat": 12345,
  "idDemanda": 30170,
  "idSetor": 1488,
  "despacho": null
}
