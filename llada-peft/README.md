# 🦙🫑 **LlaDA Parameter-efficient Cross-lingual Finetuning**

(...llada, lada, heh, get it? :harold:)

Deployed to the following [**Huggingface space**](https://spuun-llada-8b-kcv.hf.space/) as a gradio interface.  
![the space](https://files.catbox.moe/sayh5d.png)

(pls don't aboos, ts comin straight outta my pocket bruh, also, might b slow for the first message, it [cold boots](https://replicate.com/docs/reference/how-does-replicate-work#cold-boots))

The backend is deployed as a [**Replicate Cog**](https://replicate.com/spuuntries/llada-8b-kcv) (Check out my cogs [here](https://github.com/spuuntries/rp-cogs)).
![replicate page](https://files.catbox.moe/cg7yov.png)

## 👯‍♀️ **Team Members**

### 🌿 **Kecambah Toge** 🌱

| Name   | NRP        | Github                                      |
| ------ | ---------- | ------------------------------------------- |
| Faiz   | 5054231013 | [spuuntries](https://github.com/spuuntries) |
| Farhan | 5054231011 | [farhanwew](https://github.com/farhanwew)   |
| Dipo   | 5054231018 | [imdipo](https://github.com/imdipo)         |

## **Short Project Description**

This project was an exploration on the application of various Parameter-Efficient Finetuning (PEFT) methods, namely Low-Rank Adaptation (LoRA), LoRA+, and PiSSA, for the cross-lingual transfer of the novel Diffusion-based Large Language Model, LlaDA, from the domain of primarily English model to the Indonesian language.

## **Full Writeup Article**

[_Article on my blog :3_](https://www.spuun.art/blog/llada-peft/lada-en)  
~~partially shilling it too, pls read :kms:~~

## **References & Bibliography**

### References:

1. Demo derived from the [official demo](https://huggingface.co/spaces/multimodalart/LLaDA) by Apolinário Passos, adapted to work with the new backend.
2. Binxu Wang's [material](https://scholar.harvard.edu/binxuw/classes/machine-learning-scratch/materials/foundation-diffusion-generative-models) on diffusion models.

### Bibliography:

```
[1]
A. Vaswani et al., “Attention is All you Need,” in Advances in Neural Information Processing Systems, I. Guyon, U. V. Luxburg, S. Bengio, H. Wallach, R. Fergus, S. Vishwanathan, and R. Garnett, Eds., Curran Associates, Inc., 2017.
[2]
S. Nie et al., “Large Language Diffusion Models.” 2025. [Online]. Available: https://arxiv.org/abs/2502.09992
[3]
J. Wei et al., “Chain-of-Thought Prompting Elicits Reasoning in Large Language Models,” in Advances in Neural Information Processing Systems, S. Koyejo, S. Mohamed, A. Agarwal, D. Belgrave, K. Cho, and A. Oh, Eds., Curran Associates, Inc., 2022, pp. 24824–24837.
[4]
DeepSeek-AI et al., “DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning.” 2025. [Online]. Available: https://arxiv.org/abs/2501.12948
[5]
X. Wang et al., “Self-Consistency Improves Chain of Thought Reasoning in Language Models,” in The Eleventh International Conference on Learning Representations , 2023. [Online]. Available: https://openreview.net/forum?id=1PL1NIMMrw
[6]
F. Zhuang et al., “A Comprehensive Survey on Transfer Learning,” Proceedings of the IEEE, vol. 109, no. 1, pp. 43–76, 2021, doi: 10.1109/JPROC.2020.3004555.
[7]
S. Cahyawijaya et al., “Cendol: Open Instruction-tuned Generative Large Language Models for Indonesian Languages,” in Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), L.-W. Ku, A. Martins, and V. Srikumar, Eds., Bangkok, Thailand: Association for Computational Linguistics, Aug. 2024, pp. 14899–14914. doi: 10.18653/v1/2024.acl-long.796.
[8]
G. I. Winata et al., “NusaX: Multilingual Parallel Sentiment Dataset for 10 Indonesian Local Languages,” in Proceedings of the 17th Conference of the European Chapter of the Association for Computational Linguistics, A. Vlachos and I. Augenstein, Eds., Dubrovnik, Croatia: Association for Computational Linguistics, May 2023, pp. 815–834. doi: 10.18653/v1/2023.eacl-main.57.
[9]
A. F. Aji et al., “One Country, 700+ Languages: NLP Challenges for Underrepresented Languages and Dialects in Indonesia,” in Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), S. Muresan, P. Nakov, and A. Villavicencio, Eds., Dublin, Ireland: Association for Computational Linguistics, May 2022, pp. 7226–7249. doi: 10.18653/v1/2022.acl-long.500.
[10]
S. Cahyawijaya et al., “IndoNLG: Benchmark and Resources for Evaluating Indonesian Natural Language Generation,” in Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing, M.-F. Moens, X. Huang, L. Specia, and S. W. Yih, Eds., Association for Computational Linguistics, Nov. 2021, pp. 8875–8898. doi: 10.18653/v1/2021.emnlp-main.699.
[11]
B. Wilie et al., “IndoNLU: Benchmark and Resources for Evaluating Indonesian Natural Language Understanding,” in Proceedings of the 1st Conference of the Asia-Pacific Chapter of the Association for Computational Linguistics and the 10th International Joint Conference on Natural Language Processing, K.-F. Wong, K. Knight, and H. Wu, Eds., Suzhou, China: Association for Computational Linguistics, Dec. 2020, pp. 843–857. doi: 10.18653/v1/2020.aacl-main.85.
[12]
L. Owen, V. Tripathi, A. Kumar, and B. Ahmed, “Komodo: A Linguistic Expedition into Indonesia’s Regional Languages.” 2024. [Online]. Available: https://arxiv.org/abs/2403.09362
[13]
K. Khandelwal, M. Tonneau, A. M. Bean, H. R. Kirk, and S. A. Hale, “Indian-BhED: A Dataset for Measuring India-Centric Biases in Large Language Models,” in Proceedings of the 2024 International Conference on Information Technology for Social Good, in GoodIT ’24. Bremen, Germany: Association for Computing Machinery, 2024, pp. 231–239. doi: 10.1145/3677525.3678666.
[14]
Z. Chen, J. M. Zhang, M. Hort, M. Harman, and F. Sarro, “Fairness Testing: A Comprehensive Survey and Analysis of Trends,” ACM Trans. Softw. Eng. Methodol., vol. 33, no. 5, Jun. 2024, doi: 10.1145/3652155.
[15]
E. Sheng, K.-W. Chang, P. Natarajan, and N. Peng, “Societal Biases in Language Generation: Progress and Challenges,” in Proceedings of the 59th Annual Meeting of the Association for Computational Linguistics and the 11th International Joint Conference on Natural Language Processing (Volume 1: Long Papers), C. Zong, F. Xia, W. Li, and R. Navigli, Eds., Online: Association for Computational Linguistics, Aug. 2021, pp. 4275–4293. doi: 10.18653/v1/2021.acl-long.330.
[16]
Z. Han, C. Gao, J. Liu, J. Zhang, and S. Q. Zhang, “Parameter-Efficient Fine-Tuning for Large Models: A Comprehensive Survey,” Transactions on Machine Learning Research, 2024, [Online]. Available: https://openreview.net/forum?id=lIsCS8b6zj
[17]
V. Lialin, V. Deshpande, X. Yao, and A. Rumshisky, “Scaling Down to Scale Up: A Guide to Parameter-Efficient Fine-Tuning.” 2024. [Online]. Available: https://arxiv.org/abs/2303.15647
[18]
E. J. Hu et al., “LoRA: Low-Rank Adaptation of Large Language Models,” in International Conference on Learning Representations, 2022. [Online]. Available: https://openreview.net/forum?id=nZeVKeeFYf9
[19]
F. Meng, Z. Wang, and M. Zhang, “PiSSA: Principal Singular Values and Singular Vectors Adaptation of Large Language Models.” 2025. [Online]. Available: https://arxiv.org/abs/2404.02948
```
