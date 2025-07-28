# Model Documentation

## Massively Multilingual Speech (MMS): Speech-to-Text Model

### Overview
* [MMS](https://ai.meta.com/blog/multilingual-model-speech-recognition/) is a single multilingual speech recognition model that can convert speech to text and text to speech in over 1,100 languages.
* The model was proposed in the paper [Scaling Speech Technology to 1,000+ Languages](https://arxiv.org/abs/2305.13516)
* MMS is trained on a large dataset of text and audio in over 1,100 languages.
* The main dataset where this model was trained was the New Testament, which the research team was able to collect for over 1,100 languages and provided more than 32h of data per language.
* Model is able to identify more than 4,000 spoken languages.
* For more details on language supported, visit [MMS - Language Coverage](https://dl.fbaipublicfiles.com/mms/misc/language_coverage_mms.html)

#### mms-1b-all

This checkpoint is a model fine-tuned for multi-lingual ASR as part of MMS project. It is based on the Wav2Vec2 architecture and makes use of adapter models to transcribe 1000+ languages.


> - Model Name: mms-1b-all<br>
> - Model Type: Multi-Lingual Automatic Speech Recognition model<br>
> - Model path: facebook/mms-1b-all
> - Supported Languages: Covers 1,162 languages.<br>
> - Language Code Type: Follows the ISO 639-3 standard for language codes<br>
> - Audio Sampling Rate: Operates at a 16 kHz sampling rate for audio input<br>
> - No. of parameter: 1 billion<br>
> - License: CC-BY-NC 4.0 license<br>
> - Developed By: Developed and maintained by Meta<br>
> - Resources: For more details, visit the model on Hugging Face: [facebook/mms-1b-all](https://huggingface.co/facebook/mms-1b-all)


#### mms-finetuned

BCS fine-tuned the `mms-1b-all` checkpoint using [MMS's Adapter training](https://huggingface.co/blog/mms_adapters) approach for Indian low-resource languages with Biblical data  

> - Model Name: mms-finetuned<br>
> - Model Type: Multi-Lingual Automatic Speech Recognition model<br>
> - Model Path: s3://bcslamdabucket/models/mms/mms-finetuned<br>
> - Supported Languages: Bilaspuri, Bhadrawahi, Kulvi, Khezha, Bhojpuri<br>
> - Language Code Type: Follows the ISO 639-3 standard for language codes<br>
> - Audio Sampling Rate: Operates at a 16 kHz sampling rate for audio input<br>
> - Developed By: Developed by Meta and finetuned by BCS

##### Fine-tuning experiment results

- For Bhojpuri, the model was fine-tuned using the MADASR'23 dataset. Built LM with  Bhojpuri NT bible (5170 verses).
- For the remaining languages, we used our own  [Snow mountain dataset](https://huggingface.co/datasets/bridgeconn/snow-mountain).

<table>
<tr>
<th rowspan=2>Language</th><th rowspan=2>Dataset</th><th rowspan=2>Eval<br>WER</th><th colspan=2>Test (without LM)</th><th colspan=2>Test (with LM)</th></tr>
<tr><th>WER</th><th>CER</th><th>WER</th><th>CER</th></tr>

<tr>
<td>Bilaspuri</td>
<td>Train: ~ 3:50:16 hr<br>Val  : ~ 0:58:02 hr<br>Test : ~ 0:57:29 hr</td>
<td>15.15</td>
<td>16.91</td>
<td>05.10</td>
<td>12.75</td>
<td>4.40</td>
</tr>

<tr>
<td>Kulvi</td>
<td>Train: ~ 4:18:14 hr<br>Val  : ~ 1:03:24 hr<br>Test : ~ 0:56:03 hr</td>
<td>19.17</td>
<td>20.82</td>
<td>06.78</td>
<td>13.92</td>
<td>5.33</td>
</tr>

<tr>
<td>Bhadrawahi</td>
<td>Train: ~ 5:14:04 hr<br>Val  : ~ 1:18:11 hr<br>Test : ~ 0:54:48 hr</td>
<td>28.26</td>
<td>28.74</td>
<td>09.21</td>
<td>20.03</td>
<td>8.00</td>
</tr>

<tr>
<td>Khuzale</td>
<td>Total: 49 verses (~ 0:09:45 hr)</td>
<td>56.32</td>
<td>61.05</td>
<td>13.24</td>
<td>29.76</td>
<td>08.14</td>
</tr>

<tr>
<td>Bhojpuri</td>
<td>Total: 10000 audios (~ 1.5 GB)</td>
<td>21.01</td>
<td>36.05</td>
<td>10.95</td>
<td>17.50</td>
<td>6.46</td>
</tr>
</table>


###### Sample Predictions
```
Lang: Bilaspuri
Ref: तिने नदिया रे कण्डे दो किश्तियां खढ़ी रियां देखी कने मच्छुवारे तिन्हां किश्तियां जो ऊथी छड्डिने मच्छियां पकड़ने रे अपणे जाल़ा जो धोई कराँ थे
Without LM: तिने नदिया रे कण्डे दो किश्तियां खढ़ी रियां देक्खी कने मच्छुया रे तिन्हां किश्तियां जो उससी छड्डिने मच्छियां पकड़ने रे अपणे जाल़ां जो दूई कराँ थे (wer: 23.07)
With LM): तिने नदिया रे कण्डे दो किश्तियां खढ़ी रियां देक्खी कने मच्छुया रे तिन्हां किश्तियां जो ऊथी छड्डिने मच्छियां पकड़ने रे अपणे जाल़ा जो धोई कराँ थे (wer: 11.53)

Lang: Kulvi
Ref: विश्वासघाती हठी घमण्डी होर परमेश्वरै रै नी बल्कि सुख विलासा बै झ़ुरी केरनु आल़ै होंणै 
Without LM: विश्वास गाती अठी घमण्डी ोर परमेश्वरै रै नंी बल्कि सुखविलासा बै झ़ुरी केरनु आल़ै होंणै (wer: 46.66)
With LM:विश्वासघाती हठी घमण्डी होर परमेश्वरै रै नैंई बल्कि सुखविलासा बै झ़ुरी केरनु आल़ै होंणै (wer: 21.42)

Lang: Bhadrawahi
Ref: त अस कुन ज़ोम कि इश्शे पूर्वज अब्राहमे कुन मैल्लू 
Without LM: तस कुन जोम कि इश्शे पूर्वज अब्राहमे कुन मैल्लू (wer: 33.33)
With LM:त अस कुन ज़ोम कि इश्शे पूर्वज अब्राहमे कुन मैल्लू (wer: 0)

Lang: Bhojpuri
Ref: उहे बात हमनी के ओहन लोग के जरिए बतावल गइल जे लोग ओह सब के शुरु से ही घटत देखले रहलन अउर जे सुसमाचार के प्रचारक रहलन
Without LM: उहे बात हमनी के ओहन लोग के जरिय बतावल गईल जे लो ओ सब के सुरू से ही घटत देखले रहलन आउर जे सुसमाचार के परचारक रहलन (wer: 25.92)
With LM:उहे बात हमनी के ओहन लोग के जरिए बतावल गइल जे लोग उ सब के शुरु से ही घटत देखले रहलन अउर जे सुसमाचार के प्रचारक रहलन (wer: 3.70)

```


## Massively Multilingual Speech (MMS) : Text-to-Speech Models 

### Overview

* The MMS-TTS models are part of the MMS project by Meta, offering speech synthesis or text-to-speech (TTS) capabilities. 
* These models are trained on diverse datasets to provide scalable and high-quality speech synthesis.
* This model supports 1107 languages. For more details on list of supported languages, visit [MMS - Language Coverage](https://dl.fbaipublicfiles.com/mms/misc/language_coverage_mms.html)
* MMS-TTS uses the same model architecture as VITS, and separate model checkpoints are available for each of the 1100+ languages in the project.
* Each of the 1,107 supported languages has its own monolingual pre-trained TTS model, making the MMS-TTS project highly comprehensive.

#### mms-tts-< lang >

> - Model Type: Mono-Lingual TTS model<br>
> - Model path: facebook/mms-tts-< lang >
> - Supported Languages: Covers 1107 languages.<br>
> - Language Code Type: Follows the ISO 639-3 standard for language codes<br>
> - Developed By: Meta<br>
> - License: CC-BY-NC 4.0<br>
> - Resources: For more details, visit the model on Hugging Face: [facebook/mms-tts](https://huggingface.co/facebook/mms-tts)

### Finetuned mms-tts models

* Model training [reference](https://github.com/ylacombe/finetune-hf-vits)
* In BCS, we finetuned `mms-tts-hin` model for 3 new low resource languages that are similar to Hindi. 
* Traning data: Snow mountain dataset
* Each finetuned model is of size ~317MB
* Most commonly employed evaluation methods for TTS systems is conducting qualitative assessments using mean opinion scores (MOS).
* MOS is a subjective scoring system that allows human evaluators to rate the perceived quality of synthesized speech on a scale from 1 to 5.
* We manually evaluated the output of the fine-tuned models and rated them as good.

#### mms-tts-bhadrawahi

> - Model Name: mms-tts-bhadrawahi<br>
> - Model Type: Monolingual<br>
> - Function: Audio Generation (Text-to-Speech)<br>
> - Language: Bhadrawahi<br>
> - Model Path: s3://bcslamdabucket/models/mms-tts/mms-tts-bhadrawahi<br>
> - Language Code Type: Follows the ISO 639-3 standard for language codes<br>
> - Developed By: Developed by Meta and finetuned by BCS

#### mms-tts-bilaspuri

> - Model Name: mms-tts-bilaspuri<br>
> - Model Type: Monolingual<br>
> - Function: Audio Generation (Text-to-Speech)<br>
> - Language: Bilaspuri<br>
> - Model Path: s3://bcslamdabucket/models/mms-tts/mms-tts-bilaspuri<br>
> - Language Code Type: Follows the ISO 639-3 standard for language codes<br>
> - Developed By: Developed by Meta and finetuned by BCS

#### mms-tts-kulvi
> - Model Name: mms-tts-kulvi<br>
> - Model Type: Monolingual<br>
> - Function: Audio Generation (Text-to-Speech)<br>
> - Language: Kulvi<br>
> - Model Path: s3://bcslamdabucket/models/mms-tts/mms-tts-kulvi<br>
> - Language Code Type: Follows the ISO 639-3 standard for language codes<br>
> - Developed By: Developed by Meta and finetuned by BCS<br>

#### mms-tts-hin-v2
> - Model Name: mms-tts-hin-v2<br>
> - Model Type: Monolingual<br>
> - Function: Audio Generation (Text-to-Speech)<br>
> - Language: Hindi<br>
> - Model Path: s3://bcslamdabucket/models/mms-tts/mms-tts-hin-v2<br>
> - Language Code Type: Follows the ISO 639-3 standard for language codes<br>
> - Developed By: Developed by Meta and finetuned by BCS<br>
> - Speaker: Blessy<br>

#### mms-tts-hin-v3
> - Model Name: mms-tts-hin-v3<br>
> - Model Type: Monolingual<br>
> - Function: Audio Generation (Text-to-Speech)<br>
> - Language: Hindi<br>
> - Model Path: s3://bcslamdabucket/models/mms-tts/mms-tts-hin-v3<br>
> - Language Code Type: Follows the ISO 639-3 standard for language codes<br>
> - Traning data: Bible commentary dataset<br>
> - Developed By: Developed by Meta and finetuned by BCS<br>
> - Speaker: Acsah<br>


## XLSR: Cross-Lingual Speech Representation Model: Speech-to-text model

### Overview

* XLS-R (Cross-Lingual Speech Representations) is a family of multilingual speech representation models based on Facebook AI's Wav2Vec 2.0 architecture. 
* These models are pre-trained on large-scale speech data in up to 128 languages from diverse languages and fine-tuned for various downstream tasks such as automatic speech recognition (ASR), speech translation, and speaker identification.
* Built on the Wav2Vec 2.0 framework with self-supervised learning.
* Available pre-trained checkpoints can be downloaded from Hugging Face [facebook/wav2vec2-xls-r](https://huggingface.co/models?other=xls_r).
* In BCS, we fine-tuned the checkpoint `wav2vec2-xls-r-1b` for low resource languages using Snow Mountain dataset. [Reference](https://huggingface.co/blog/fine-tune-xlsr-wav2vec2) 

### Fine-tuned models

* Fine-tuned the base model for few gateway languages (Hindi, Malayalam, Kannada, Tamil, Telugu) and Hindi minority languags (Haryanvi, Bilaspuri, Dogri, Gaddi, Bhadrawahi, Kangri, Kulvi, Mandeali, Pahari Mahasui and Kulvi outer seraji)

> - Model Name: stt-xlsr-< lang ><br>
> - Base Model: wav2vec2-xls-r-1b<br>
> - Model Type: Monolingual<br>
> - Function: Speech-to-text, transcription<br>
> - Model Path: s3://bcslamdabucket/models/xlsr/< model-name ><br>
> - Language Code Type: Follows the ISO 639-3 standard for language codes<br>
> - License: apache-2.0<br>
> - Developed By: Developed by Meta and finetuned by BCS

##### Fine-tuning experiment results

- For Bhojpuri, the model was fine-tuned using the MADASR'23 dataset. Built LM with  Bhojpuri NT bible (5170 verses).
- For the remaining languages, we used our own  [Snow mountain dataset](https://huggingface.co/datasets/bridgeconn/snow-mountain).

<table>
<tr>
<th rowspan=2>Language</th><th rowspan=2>Dataset</th><th rowspan=2>Eval<br>WER</th><th colspan=2>Test (without LM)</th><th colspan=2>Test (with LM)</th></tr>
<tr><th>WER</th><th>CER</th><th>WER</th><th>CER</th></tr>

<tr>
<td>Hindi</td>
<td>11511 audios (~ 22.60 hr)</td>
<td>3.59</td>
<td>3.66</td>
<td>1.08</td>
<td>2.38</td>
<td>0.86</td>
</tr>

<tr>
<td>Haryanvi</td>
<td>3037 audios (~ 6.29 hr)</td>
<td>25.63</td>
<td>23.87</td>
<td>11.48</td>
<td>20.65</td>
<td>11.14</td>
</tr>

<tr>
<td>Bilaspuri</td>
<td>3022 audios (~ 6.19 hr)</td>
<td>14.40 </td>
<td>16.08</td>
<td>5.01</td>
<td>13.02</td>
<td>4.54</td>
</tr>

<tr>
<td>Dogri</td>
<td>4578 audios (~ 9.14 hr)</td>
<td>13.74</td>
<td>13.59</td>
<td>4.68</td>
<td>11.72</td>
<td>4.32</td>
</tr>

<tr>
<td>Kulvi</td>
<td>3319 audios (~ 6.76 hr)</td>
<td>-</td>
<td>16.77</td>
<td>5.71</td>
<td>-</td>
<td>-</td>
</tr>

<tr>
<td>Bhadrawahi</td>
<td>4114 audios (~ 8.10 hr)</td>
<td>-</td>
<td>19.48</td>
<td>6.91</td>
<td>-</td>
<td>-</td>
</tr>

<tr>
<td>Gaddi</td>
<td>4769 audios (~ 9.31 hr)</td>
<td>-</td>
<td>14.47</td>
<td>4.74</td>
<td>-</td>
<td>-</td>
</tr>

<tr>
<td>Kangri</td>
<td>4368 audios (~ 8.65 hr)</td>
<td>-</td>
<td>11.16</td>
<td>3.79</td>
<td>-</td>
<td>-</td>
</tr>

<tr>
<td>Mandeali</td>
<td>3353 audios (~ 6.83 hr)</td>
<td>-</td>
<td>12.67</td>
<td>4.19</td>
<td>-</td>
<td>-</td>
</tr>

<tr>
<td>Pahari mahasui</td>
<td>4430 audios (~ 8.68 hr)</td>
<td>-</td>
<td>14.33</td>
<td>4.77</td>
<td>-</td>
<td>-</td>
</tr>

<tr>
<td>Malayalam</td>
<td>18225 audios (~ 32:09:02 hr)</td>
<td>14.48</td>
<td>13.83</td>
<td>2.03</td>
<td>13.07</td>
<td>1.94</td>
</tr>

<tr>
<td>Kannada</td>
<td>14559 audios (~ 26:33:17 hr)</td>
<td>12.83</td>
<td>13.55</td>
<td>1.98</td>
<td>12.87</td>
<td>1.86</td>
</tr>

<tr>
<td>Tamil</td>
<td>14841 audios (~ 27:05:03 hr)</td>
<td>12.55</td>
<td>12.14</td>
<td>1.53</td>
<td>13.17</td>
<td>1.67</td>
</tr>

<tr>
<td>Telugu</td>
<td>13606 audios (~ 25:32:19 hr)</td>
<td>16.98</td>
<td>16.68</td>
<td>3.06</td>
<td>14.77</td>
<td>2.82</td>
</tr>

<tr>
<td>Bhojpuri</td>
<td>10000 audios (~ 1.5 GB)</td>
<td>19.32</td>
<td>49.63</td>
<td>16.97</td>
<td>35.85</td>
<td>13.52</td>
</tr>

<tr>
<td>Khuzale</td>
<td>10000 audios (~ 1.5 GB)</td>
<td>63.30</td>
<td>61.71</td>
<td>13.76</td>
<td>53.82</td>
<td>12.60</td>
</tr>

</table>


##### Comparison of fine-tuned MMS model with fine-tuned XLSR model

<table>
    <tr>
        <th rowspan="2">Language</th>
        <th colspan="2" style="text-align:center;">MMS (w/o LM)</th>
        <th colspan="2" style="text-align:center;">XLSR (w/o LM)</th>
    </tr>
    <tr>
        <th>Test WER </th>
        <th>Test CER</th>
        <th>Test WER</th>
        <th>Test CER</th>
    </tr>
    <tr>
        <td>Bilaspuri</td>
        <td>16.91</td>
        <td>5.10</td>
        <td>16.08</td>
        <td>5.01</td>
    </tr>
    <tr>
        <td>Bhadrawahi</td>
        <td>28.74</td>
        <td>9.21</td>
        <td>19.48</td>
        <td>6.91</td>
    </tr>
    <tr>
        <td>Kulvi</td>
        <td>20.82</td>
        <td>6.78</td>
        <td>16.77</td>
        <td>5.71</td>
    </tr>
    <tr>
        <td>Bhojpuri</td>
        <td>36.05</td>
        <td>10.95</td>
        <td>49.63</td>
        <td>16.97</td>
    </tr>
</table>

## No Language Left Behind (NLLB): Text Translation Model

### Overview

* No Language Left Behind ([NLLB](https://ai.meta.com/research/no-language-left-behind/)) is a first-of-its-kind, AI breakthrough project that open-sources models capable of delivering evaluated, high-quality translations directly between 200 languages—including low-resource languages like Asturian, Luganda, Urdu and more. 
* It aims to give people the opportunity to access and share web content in their native language, and communicate with anyone, anywhere, regardless of their language preferences.
* The model primarily intended for research in machine translation, especially for low-resource languages. It allows for `single sentence translation` among 200 languages.
* The model was trained with input lengths not exceeding `512 tokens`, therefore translating longer sequences might result in quality degradation.

> - Model Type: Multilingual<br>
> - Function: Text Translation<br>
> - Text Input Length: < 512 tokens<br>
> - Supported Languages: 200+ languages.For a comprehensive list of supported languages, refer [FLORES-200](https://github.com/facebookresearch/flores/blob/main/flores200/README.md)<br>
> - Language Code Type: BCP-47<br>
> - Developed By: Developed by Meta<br>
> - License: CC-BY-NC 4.0

#### nllb-200-distilled-600M

This model is a smaller and faster variant of the NLLB model family, making it suitable for real-time applications.

> - Model Name: nllb-200-distilled-600M<br>
> - Model Path: facebook/nllb-200-distilled-600M<br>
> - No. of parameter: 600M <br>
> - Resources: For more details, visit the model on Hugging Face: [facebook/nllb-200-distilled-600M](https://huggingface.co/facebook/nllb-200-distilled-600M)


#### nllb-200-distilled-1.3B

This model is a more powerful variant of the NLLB model family, offering higher accuracy and robustness.

> - Model Name: nllb-200-distilled-1.3B<br>
> - Model Path: facebook/nllb-200-distilled-1.3B<br>
> - No. of parameter: 1.3 billion<br>
> - Resources: For more details, visit the model on Hugging Face: [facebook/nllb-200-distilled-1.3B](https://huggingface.co/facebook/nllb-200-distilled-1.3B)


##### Sample translations:
```
Source Text: जब वह इन बातों की सोच ही में था तो परमेश्‍वर का स्वर्गदूत उसे स्वप्न में दिखाई देकर कहने लगा, “हे यूसुफ! दाऊद की सन्तान, तू अपनी पत्‍नी मरियम को अपने यहाँ ले आने से मत डर, क्योंकि जो उसके गर्भ में है, वह पवित्र आत्मा की ओर से है।
Source lang: Hindi
Target lang: Tamil
Prediction: ஆனால் அவர் இவ்வாறு யோசித்தபோது, ஒரு தேவ தூதர் கனவில் அவருக்குக் காட்சி அளித்து, \"தாவீதின் மகனே, மரியாளை உம்மோடு சேர்த்துக்கொள்ள அஞ்சாதே. ஏனெனில், அவள் கர்ப்பம் பரிசுத்த ஆவியின் வழியாகவே ஏற்பட்டுள்ளது.

Source Text: जब वह इन बातों की सोच ही में था तो परमेश्‍वर का स्वर्गदूत उसे स्वप्न में दिखाई देकर कहने लगा, “हे यूसुफ! दाऊद की सन्तान, तू अपनी पत्‍नी मरियम को अपने यहाँ ले आने से मत डर, क्योंकि जो उसके गर्भ में है, वह पवित्र आत्मा की ओर से है।
Source lang: Hindi
Target lang: Bhojpuri
Prediction: मुला अइसा भवा कि ओकरे मन मँ अइसा ही विचार होइ गवा कि परमेस्सर क एक दूत स्वप्नात परगट होइके ओसे कहेस ", यूसुफ, दाऊद क पूत, मरियम क संग बियाह करइ स जिन डेराअ काहेकि ओके गरभ मँ पवित्तर आतिमा स मिला बा।"

```

## SeamlessM4T (Massively Multilingual & Multimodal Machine Translation)

### Overview

* [SeamlessM4T](https://ai.meta.com/blog/seamless-m4t/) is a comprehensive collection of models designed to facilitate high-quality multilingual translation, bridging communication gaps between diverse linguistic communities. It provides an integrated solution for speech and text translation tasks, eliminating the need for separate models for each task.
* SeamlessM4T supports the following tasks:
   - Speech-to-Speech Translation (S2ST)
   - Speech-to-Text Translation (S2TT)
   - Text-to-Speech Translation (T2ST)
   - Text-to-Text Translation (T2TT)
   - Automatic Speech Recognition (ASR)
* Model is capable of performing all the above tasks within a single model.
* For more details, refer the paper:[SeamlessM4T—Massively Multilingual & Multimodal Machine Translation](https://dl.fbaipublicfiles.com/seamless/seamless_m4t_paper.pdf)

#### seamless-m4t-v2-large
Multimodal and multilingual translation model developed by Meta. It facilitates seamless communication across languages by integrating multiple tasks within a single model. Designed for speech and text processing, it supports a wide range of languages and is optimized for high-quality translations and transcriptions.

> - Model Name: seamless-m4t-v2-large<br>
> - Model Type: Multi-modal multilingual<br>
> - Function: Multimodal translation and synthesis<br>
> - Supported Languages: Model covers 100 languages for Speech Input, Text Input, and Text Output. 36 languages are covered for Speech output.<br>
> - Audio Sampling Rate: 16 kHz<br>
> - Model Path: facebook/seamless-m4t-v2-large<br>
> - Language Code Type: ISO 639-3<br>
> - Developed By: Meta<br>
> - License: CC-BY-NC 4.0<br>
> - Resources: For more details, visit the model on Hugging Face: [facebook/seamless-m4t-v2-large](https://huggingface.co/facebook/seamless-m4t-v2-large)

## OpenVoice

### Overview
* OpenVoice is a versatile instant voice cloning approach that requires only a short audio clip from the reference speaker to replicate their voice and generate speech in multiple languages. 
* It enables granular control over voice styles, including emotion, accent, rhythm, pauses, and intonation, in addition to replicating the tone color of the reference speaker.
* The reference voice and the generated voice can be in any languages outside the massive-speaker multi-lingual dataset.
* For more details, refer [Open Voice](https://research.myshell.ai/open-voice)

> - Model Name: openvoice-v2<br>
> - Function: Voice Cloning  and Voice Conversion  <br>
> - Languages: Multilingual<br>
> - Model Path: s3://bcslamdabucket/models/openvoice-v2/converter<br>
> - License: MIT License <br>
> - Developed By: MyShell-AI

## DeepFilterNet

### Overview
* The DeepFilterNet model is a powerful tool designed for real-time noise suppression in audio processing. 
* Its efficient architecture enables it to handle challenging environments, making it ideal for applications like telecommunication, broadcasting, and speech enhancement.
* For more details, refer the github repository [DeepFilterNet](https://github.com/Rikorose/DeepFilterNet)

> - Model Name: DeepFilterNet3<br>
> - Function: Noise removal <br>
> - Languages: Multilingual<br>
> - Model Path: s3://bcslamdabucket/models/DeepFilterNet3<br>
> - License: apache-2.0, MIT License<br>
> - Audio sampling rate: 48kHz

## inaSpeechSegmenter

### Overview
* inaSpeechSegmenter is a CNN-based audio segmentation toolkit suited to the tasks of Voice Activity Detection and Speaker Gender Segmentation.
* It splits audio signals into homogeneous zones of speech, music ,noise and silence. 
* Zones corresponding to speech over music or speech over noise are tagged as speech. 
* Singing voice is tagged as music.
* For more details, refer the github repository [inaSpeechSegmenter](https://github.com/ina-foss/inaSpeechSegmenter)

> - Model Name: InaSpeechSegmenter<br>
> - Function: audio-segmentation, voice activity detection, VAD<br>
> - License: MIT License<br>
> - Model Path: s3://bcslamdabucket/models/audio-segmentation<br>
> - Developed By: L'Institut National de l'Audiovisuel<br>
> - Audio sampling rate: 16kHz

## MMS-FA

### Overview
* MMS-FA accurately aligns the audio recordings with their corresponding textual transcriptions at the sentence level, ensuring precise time-stamped synchronization between the spoken content and its written form.
* It uses TorchAudio’s high-level API, torchaudio.pipelines.Wav2Vec2FABundle, which packages the pre-trained model, tokenizer and aligner.
* The waveform is passed to an acoustic model, which produces the sequence of probability distribution of tokens.
* The transcript is passed to tokenizer, which converts the transcript to sequence of tokens. 
* Aligner takes the results from the acoustic model and the tokenizer and generate timestamps for each token.
* For more details, refer the document [MMS-FA](https://pytorch.org/audio/stable/tutorials/forced_alignment_tutorial.html)

> - Model Name: MMS-FA<br>
> - Function: forced alignment<br>
> - License: BSD 2-Clause <br>
> - Developed By: Meta<br>
> - Languages: Multilingual<br>

## Resemble-enhance

### Overview
* [Resemble Enhance](https://github.com/resemble-ai/resemble-enhance) is an AI-powered tool which improves the overall quality of speech. 
* It consists of two modules: a denoiser, which separates speech from a noisy audio, and an enhancer, which further boosts the perceptual audio quality by restoring audio distortions and extending the audio bandwidth
* The denoiser uses a UNet model.
* The enhancer is a latent conditional flow matching (CFM) model.

> - Model Name: resemble-enhance<br>
> - Function: audio enhancement<br>
> - License: MIT license <br>
> - Developed By: resemble-ai<br>
> - Languages: Multilingual<br>

## chatterbox

### Overview
* [chatterbox](https://github.com/resemble-ai/chatterbox) is Resemble AI's first production-grade open source TTS model that delivers state-of-the-art zero-shot text-to-speech synthesis and voice cloning capabilities.
* The model supports voice cloning through audio prompts, allowing users to synthesize speech in any target voice by providing a reference audio sample.
* The model is trained on 0.5M hours of cleaned data and uses alignment-informed inference for ultra-stable performance.

> - Model Name: chatterbox<br>
> - Function: text-to-speech synthesis and voice conversion<br>
> - License: MIT license <br>
> - Developed By: resemble-ai<br>
> - Languages: Multilingual<br>