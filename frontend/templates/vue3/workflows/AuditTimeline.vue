<template><div class="pf-card"><h3>{{ AuditedEntity }} History</h3>
<div class="pf-toolbar"><input v-model="id" placeholder="Entity ID" class="pf-input"/><button class="pf-btn" @click="load">Load</button><button class="pf-btn pf-primary" @click="bump">Bump Version</button></div>
<ul class="pf-timeline"><li v-for="h in history" :key="h.id"><strong>#{{ h.version }}</strong> – {{ h.changedAt }} – {{ h.changedBy || "system" }}<pre class="pf-pre">{{ h.diff }}</pre></li></ul></div></template>
<script setup>
import { ref } from "vue"; import { createGraphQLClient } from "../composables/useGraphQL";
const props=defineProps({ endpoint:{type:String,default:""} }); const client=createGraphQLClient(props.endpoint);
const id=ref(""); const history=ref([]);
const Q=`query($id:ID!){ {{ audited_entity_field }}(id:$id){ id history{ id version changedAt changedBy diff } } }`; const M=`mutation($id:ID!){ {{ bump_version_field }}(id:$id){ id version } }`;
async function load(){ const d=await client.request(Q,{id:id.value}); history.value=d["{{ audited_entity_field }}"]?.history??[]; }
async function bump(){ await client.request(M,{id:id.value}); await load(); }
</script>
<style scoped>.pf-card{border:1px solid #ddd;border-radius:12px;padding:12px}.pf-toolbar{display:flex;gap:8px;margin-bottom:8px}.pf-input{padding:8px;border:1px solid #ccc;border-radius:8px}.pf-btn{padding:6px 10px;border:1px solid #ccc;border-radius:8px;background:#f8f8f8;cursor:pointer}.pf-primary{border-color:#1f6feb}.pf-timeline{list-style:none;padding:0}.pf-pre{background:#fafafa;border:1px solid #eee;border-radius:8px;padding:8px;overflow:auto}</style>
