<template>
  <div v-if="open" class="pf-modal-backdrop" @click.self="close">
    <div class="pf-modal">
      <h3>{{ isEdit ? "Edit {{ Entity }}" : "New {{ Entity }}" }}</h3>
      <form @submit.prevent="save">
        {% if code_field %}<label>{{ code_field|capitalize }}<input v-model="form.{{ code_field }}" required class="pf-input"/></label>{% endif %}
        <label>Name<input v-model="form.name" required class="pf-input"/></label>
        <div class="pf-actions">
          <button type="button" class="pf-btn" @click="close">Cancel</button>
          <button type="submit" class="pf-btn pf-primary">Save</button>
        </div>
      </form>
    </div>
  </div>
</template>
<script setup>
import { reactive, watch, computed } from "vue";
import { createGraphQLClient } from "../composables/useGraphQL";
import { useCatalogs } from "../composables/useCatalogs";
const props = defineProps({ endpoint:{type:String,default:""}, open:{type:Boolean,default:false}, value:{type:Object,default:null} });
const emit = defineEmits(["close","saved"]);
const client = createGraphQLClient(props.endpoint);
const { create, update } = useCatalogs({ client, Entity: "{{ Entity }}" });
const isEdit = computed(()=>!!props.value?.id);
const form = reactive({ id:null, {% if code_field %}{{ code_field }}:"",{% endif %} name:"" });
watch(()=>props.value,(v)=>{ if(v) Object.assign(form,v); else { form.id=null; {% if code_field %}form.{{ code_field }}="";{% endif %} form.name=""; } },{immediate:true});
function close(){ emit("close"); }
async function save(){ const payload = { {% if code_field %}{{ code_field }}: form.{{ code_field }}, {% endif %} name: form.name }; const result = isEdit.value ? await update(form.id, payload) : await create(payload); emit("saved", result); close(); }
</script>
<style scoped>
.pf-modal-backdrop{position:fixed;inset:0;background:rgba(0,0,0,.3);display:grid;place-items:center}
.pf-modal{width:420px;max-width:92vw;background:#fff;border-radius:12px;padding:16px}
.pf-input{width:100%;padding:8px;border:1px solid #ccc;border-radius:8px}
label{display:block;margin:8px 0}.pf-actions{display:flex;justify-content:flex-end;gap:8px;margin-top:12px}
.pf-btn{padding:6px 10px;border:1px solid #ccc;border-radius:8px;background:#f8f8f8;cursor:pointer}.pf-primary{border-color:#1f6feb}
</style>
