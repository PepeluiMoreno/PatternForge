<template><div class="pf-card"><h3>Integrity Validation</h3>
<form @submit.prevent="validateUnique"><div class="pf-grid2"><div v-for="f in uniqueFields" :key="f"><label>{{ f }}<input v-model="uniquePayload[f]" class="pf-input"/></label></div></div>
<div class="pf-actions"><button class="pf-btn pf-primary" type="submit">Validate Unique</button><span v-if="uniqueResult!==null" :class="uniqueResult ? 'ok':'ko'">{{ uniqueResult ? 'OK' : 'Conflict' }}</span></div></form>
<hr/>
<form @submit.prevent="validateReference"><div class="pf-grid2"><label>Field<input v-model="ref.field" class="pf-input"/></label><label>Value<input v-model="ref.value" class="pf-input"/></label><label>Reference<input v-model="ref.reference" class="pf-input"/></label><label>Reference Field<input v-model="ref.referenceField" class="pf-input"/></label></div>
<div class="pf-actions"><button class="pf-btn" type="submit">Validate Reference</button><span v-if="refResult!==null" :class="refResult ? 'ok':'ko'">{{ refResult ? 'Exists' : 'Not Found' }}</span></div></form></div></template>
<script setup>
import { reactive, ref } from "vue"; import { createGraphQLClient } from "../composables/useGraphQL";
const props=defineProps({ endpoint:{type:String,default:""}, uniqueFields:{type:Array,default:()=>["code","name"]} });
const client=createGraphQLClient(props.endpoint); const uniquePayload=reactive({}); const uniqueResult=ref(null); const ref=reactive({ field:"", value:"", reference:"", referenceField:"" }); const refResult=ref(null);
async function validateUnique(){ const argsDecl=props.uniqueFields.map(f=>`$${f}: String!`).join(","); const argsPass=props.uniqueFields.map(f=>`${f}: $${f}`).join(","); const query=`mutation(${argsDecl}){ {{ validate_unique_field }}(${argsPass}) }`; const data=await client.request(query, uniquePayload); uniqueResult.value=data["{{ validate_unique_field }}"]; }
const MR=`mutation($field:String!,$value:String!,$reference:String!,$referenceField:String!){ {{ validate_reference_field }}(field:$field,value:$value,reference:$reference,referenceField:$referenceField) }`;
async function validateReference(){ const data=await client.request(MR, ref); refResult.value=data["{{ validate_reference_field }}"]; }
</script>
<style scoped>.pf-card{border:1px solid #ddd;border-radius:12px;padding:12px}.pf-grid2{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:8px}label{display:block}.pf-input{width:100%;padding:8px;border:1px solid #ccc;border-radius:8px}.pf-actions{display:flex;align-items:center;gap:8px;margin-top:8px}.ok{color:#0a7}.ko{color:#d33}.pf-btn{padding:6px 10px;border:1px solid #ccc;border-radius:8px;background:#f8f8f8;cursor:pointer}.pf-primary{border-color:#1f6feb}</style>
