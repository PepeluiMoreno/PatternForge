<template><div class="pf-card"><h3>{{ WorkflowEntity }} States</h3>
<div class="pf-tabs"><button v-for="s in states" :key="s" class="pf-tab" :class="{active: s===state}" @click="state=s">{{ s }}</button></div>
<ul><li v-for="item in rows" :key="item.id">{{ item.id }} – {{ item.state }}</li></ul>
<div class="pf-actions"><input v-model="transitionId" placeholder="Entity ID" class="pf-input"/><select v-model="to" class="pf-input"><option v-for="s in states" :key="s" :value="s">{{ s }}</option></select><button class="pf-btn pf-primary" @click="transition">Transition</button></div></div></template>
<script setup>
import { ref, watch, onMounted } from "vue"; import { createGraphQLClient } from "../composables/useGraphQL";
const props=defineProps({ endpoint:{type:String,default:""}, states:{type:Array,default:()=>[{% for s in states %}"{{ s }}",{% endfor %}] } });
const client=createGraphQLClient(props.endpoint); const state=ref(props.states[0]); const rows=ref([]); const transitionId=ref(""); const to=ref(props.states[0]);
const LIST=`query($state:{{ StateEnum }}){ {{ workflow_entities_field }}(state:$state){ id state } }`; const MUT=`mutation($id:ID!,$to:{{ StateEnum }}!){ {{ transition_field }}(id:$id,to:$to){ id state } }`;
async function load(){ const d=await client.request(LIST,{state:state.value}); rows.value=d["{{ workflow_entities_field }}"]; }
async function transition(){ await client.request(MUT,{id:transitionId.value,to:to.value}); await load(); }
watch(state,load); onMounted(load);
</script>
<style scoped>.pf-card{border:1px solid #ddd;border-radius:12px;padding:12px}.pf-tabs{display:flex;gap:6px;margin-bottom:8px}.pf-tab{padding:6px 10px;border:1px solid #ccc;border-radius:8px;background:#f8f8f8;cursor:pointer}.pf-tab.active{border-color:#1f6feb}.pf-actions{display:flex;gap:8px;margin-top:12px}.pf-input{padding:8px;border:1px solid #ccc;border-radius:8px}.pf-btn{padding:6px 10px;border:1px solid #ccc;border-radius:8px;background:#f8f8f8;cursor:pointer}.pf-primary{border-color:#1f6feb}</style>
