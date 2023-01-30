import streamlit as st 

from torchtyping import TensorType as TT
from transformer_lens.hook_points import HookPoint
from .environment import get_action_preds
from .visualizations import plot_action_preds, plot_single_residual_stream_contributions
from .analysis import get_residual_decomp

def show_ablation(dt, logit_dir):

    with st.expander("Ablation Experiment"):
        st.write("ablation experiment here")
        # list out the components of the transformer

        # make a streamlit form for choosing a component to ablate
        n_layers = dt.n_layers
        n_heads = dt.n_heads

        columns = st.columns(4)
        with columns[0]:
            layer = st.selectbox("Layer", list(range(n_layers)))
        with columns[1]:
            component = st.selectbox("Component", ["MLP", "HEAD"], index=1)
        with columns[2]:
            if component == "HEAD":
                head = st.selectbox("Head", list(range(n_heads)))
        with columns[3]:
            ablate_to_mean = st.checkbox("Ablate to mean", value = True)

        if component == "HEAD":
            ablation_func = get_ablation_function(ablate_to_mean, head)
            dt.transformer.blocks[layer].attn.hook_z.add_hook(ablation_func)
            st.write(dt.transformer.blocks[layer].attn.hook_z)
            action_preds, x, cache, tokens = get_action_preds(dt)
            plot_action_preds(action_preds) 
            if st.checkbox("show counterfactual residual contributions"):
                residual_decomp = get_residual_decomp(dt, cache, logit_dir)
                plot_single_residual_stream_contributions(residual_decomp)




        # once selected, do a forward pass with the ablation



    # then, render a single residual stream contribution with the ablation

def get_ablation_function(ablate_to_mean, head_to_ablate):

    def head_ablation_hook(
        value: TT["batch", "pos", "head_index", "d_head"],
        hook: HookPoint
    ) -> TT["batch", "pos", "head_index", "d_head"]:
        print(f"Shape of the value tensor: {value.shape}")

        if ablate_to_mean:
            value[:, :, head_to_ablate, :] = value[:, :, head_to_ablate, :].mean(dim = 2, keepdim = True)
        else:
            value[:, :, head_to_ablate, :] = 0.
        return value

    return head_ablation_hook