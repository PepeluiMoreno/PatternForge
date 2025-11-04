<template>
  <div class="pf-card">
    <div class="pf-toolbar">
      <input v-model="search" placeholder="Search {{ Entity }}..." class="pf-input" @keyup.enter="load"/>
      <button class="pf-btn" @click="load">Search</button>
      <button class="pf-btn pf-primary" @click="$emit('create')">New</button>
    </div>
    <table class="pf-table">
      <thead><tr><th>ID</th>{% if code_field %}<th>{{ code_field|capitalize }}</th>{% endif %}<th>Name</th><th class="pf-right">Actions</th></tr></thead>
      <tbody>
        <tr v-for="row in rows" :key="row.id">
          <td>{{ row.id }}</td>
          {% if code_field %}<td>{{ row.{{ code_field }} }}</td>{% endif %}
          <td>{{ row.name }}</td>
          <td class="pf-right">
            <button class="pf-btn" @click="$emit('edit', row)">Edit</button>
            <button class="pf-btn pf-danger" @click="$emit('delete', row)">Delete</button>
          </td>
        </tr>
      </tbody>
    </table>
    <div class="pf-footer">
      <button class="pf-btn" :disabled="offset===0" @click="prev">Prev</button>
      <span>{{ offset + 1 }}–{{ Math.min(offset + limit, totalHint) }} (≈)</span>
      <button class="pf-btn" :disabled="rows.length < limit" @click="next">Next</button>
    </div>
  </div>
</template>
<script setup>
import { ref, onMounted } from "vue";
import { createGraphQLClient } from "../composables/useGraphQL";
import { useCatalogs } from "../composables/useCatalogs";
const props = defineProps({ endpoint: { type: String, default: "" }, limit: { type: Number, default: 20 } });
const emit = defineEmits(["create", "edit", "delete"]);
const client = createGraphQLClient(props.endpoint);
const { list } = useCatalogs({ client, Entity: "{{ Entity }}" });
const rows = ref([]); const search = ref(""); const offset = ref(0); const limit = ref(props.limit); const totalHint = ref(9999);
async function load(){ rows.value = await list({ search: search.value, offset: offset.value, limit: limit.value }); }
function next(){ offset.value += limit.value; load(); } function prev(){ offset.value = Math.max(0, offset.value - limit.value); load(); }
onMounted(load);
</script>
<style scoped>
.pf-card{border:1px solid #ddd;border-radius:12px;padding:12px;background:#fff}
.pf-toolbar{display:flex;gap:8px;margin-bottom:8px}
.pf-input{flex:1;padding:8px;border:1px solid #ccc;border-radius:8px}
.pf-btn{padding:6px 10px;border:1px solid #ccc;border-radius:8px;background:#f8f8f8;cursor:pointer}
.pf-btn:hover{background:#f0f0f0}
.pf-primary{border-color:#1f6feb}.pf-danger{border-color:#d73a49}
.pf-table{width:100%;border-collapse:collapse}
.pf-table th,.pf-table td{border-bottom:1px solid #eee;text-align:left;padding:8px}
.pf-right{text-align:right}
.pf-footer{display:flex;justify-content:space-between;margin-top:8px;align-items:center}
</style>
