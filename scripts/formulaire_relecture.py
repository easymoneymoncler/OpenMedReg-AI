"""Formulaire PDF de relecture à l'aveugle des verdicts d'un juge sur un cas fictif.

Le relecteur voit chaque exigence, le verdict de l'outil, ses citations et sa
justification, mais jamais le corrigé : son avis est indépendant. Le script
écrit une source LaTeX ; la compiler avec ``pdflatex`` (deux passes).

    python scripts/formulaire_relecture.py eval/cases/fictif-therm-t1 \
        results/2026-11-11_fictif-therm-t1/fictif-therm-t1.gemma4-31b.jsonl \
        --out results/2026-11-11_fictif-therm-t1/formulaire_relecteur.tex
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import yaml

from openmedreg.gap_analysis import load_units, requirements_in_scope

LIBELLE = {
    "conforme": "conforme",
    "non_conforme": "non conforme",
    "non_trouve": "non trouvé",
    "non_applicable": "non applicable",
}


def esc(s: str) -> str:
    rep = {
        "\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#",
        "_": r"\_", "{": r"\{", "}": r"\}", "~": r"\textasciitilde{}", "^": r"\^{}",
        "°": r"\textdegree{}", "±": r"$\pm$", "×": r"$\times$", ">": r"\textgreater{}",
        "<": r"\textless{}", "→": r"$\rightarrow$", "≤": r"$\leq$", "≥": r"$\geq$",
    }
    return "".join(rep.get(c, c) for c in s)


def box(name: str) -> str:
    return (rf"\CheckBox[name={name},width=1.05em,height=1.05em,"
            r"bordercolor={0 0 0},borderwidth=1]{}")


def field(name: str, height: str) -> str:
    return (rf"\TextField[name={name},multiline=true,width=\linewidth,height={height},"
            r"bordercolor={0.6 0.6 0.6},borderwidth=0.5]{}")


def line_field(name: str, width: str = "7cm") -> str:
    return (rf"\TextField[name={name},width={width},height=1.3em,"
            r"bordercolor={0.6 0.6 0.6},borderwidth=0.5]{}")


def dossier_latex(md: str) -> str:
    out = []
    for raw in md.splitlines():
        line = raw.strip()
        if not line:
            out.append("")
            continue
        if line.startswith("### "):
            out.append(rf"\par\medskip{{\small\bfseries {esc(line[4:])}}}\par")
        elif line.startswith("## "):
            out.append(rf"\par\medskip{{\normalsize\bfseries {esc(line[3:])}}}\par")
        elif line.startswith("# "):
            out.append(rf"\par\medskip{{\large\bfseries {esc(line[2:])}}}\par")
        elif line.startswith("> "):
            out.append(rf"{{\small\itshape {esc(line[2:])}}}\par")
        elif line.startswith("- "):
            out.append(rf"{{\small\textbullet\ {esc(line[2:])}}}\par")
        else:
            out.append(rf"{{\small {esc(line)}}}\par")
    return "\n".join(out)


def first_line(s: str) -> str:
    return s.split("\n", 1)[0].strip()


def shorten(s: str, n: int = 320) -> str:
    s = re.sub(r"\s+", " ", s).strip()
    return s if len(s) <= n else s[:n].rsplit(" ", 1)[0] + "…"


PREAMBULE = r"""\pdfobjcompresslevel=0
\documentclass[11pt,a4paper]{article}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage[french]{babel}
\usepackage[margin=2.1cm]{geometry}
\usepackage{xcolor}
\usepackage{enumitem}
\usepackage{fancyhdr}
\usepackage[colorlinks=false,pdfborder={0 0 0}]{hyperref}
\setlist{nosep,leftmargin=1.4em}
\setlength{\parindent}{0pt}\setlength{\parskip}{6pt}
\pagestyle{fancy}\fancyhf{}
\lhead{\small OpenMedReg-AI --- relecture à l'aveugle}\rhead{\small dossier FICTIF}\cfoot{\small\thepage}
\definecolor{gris}{gray}{0.35}
\newcommand{\rub}[1]{\par\medskip{\bfseries\color{gris}#1}\par}
\begin{document}
\begin{Form}
"""


def accueil(case: str, n: int, juge: str) -> str:
    return rf"""
\begin{{center}}
{{\LARGE\bfseries Formulaire de relecture}}\\[4pt]
{{\large Un outil d'IA face à l'Annexe II du MDR : a-t-il raison ?}}\\[4pt]
{{\small Cas \texttt{{{esc(case)}}} --- {n} exigences --- tout est dans ce PDF, aucune connexion nécessaire}}
\end{{center}}

\rub{{Le contexte}}
OpenMedReg-AI est un projet open source d'aide à la relecture réglementaire. Pour chaque exigence
de l'Annexe II du règlement (UE) 2017/745 (documentation technique), l'outil cherche dans un dossier
technique le passage qui y répond, le cite mot pour mot et propose un verdict. Ici, il a analysé un
dossier \textbf{{entièrement fictif}} (un capteur de température cutané inventé), qui contient des lacunes
volontaires. L'outil aide à la relecture ; il ne délivre pas d'avis de conformité, et ce formulaire non plus.

\rub{{Ce qu'on vous demande}}
Dire, pour chacune des {n} exigences, quel est selon vous le bon verdict, et si le passage cité par l'outil
le justifie. Vous ne voyez pas le corrigé préparé de notre côté, pour que votre avis reste indépendant :
c'est lui qui servira de référence. Il n'y a pas de piège, et « je ne peux pas trancher » est une réponse utile.

\rub{{Comment remplir}}
\begin{{enumerate}}
\item Lisez d'abord le dossier fictif (pages suivantes, environ 15 minutes).
\item Puis une page par exigence : l'exigence, la réponse de l'outil, et trois questions à cocher.
  Cochez une seule case par question. La remarque est facultative.
\item Si les cases ne se cochent pas dans votre lecteur de PDF (certains lecteurs de téléphone), notez
  vos réponses à part sous la forme « 12 : Q1 non conforme, Q2 non, Q3 sûre ».
\item \textbf{{Enregistrez}} le PDF de temps en temps. Durée estimée : 1 h 15 à 1 h 45, en plusieurs fois si besoin.
\end{{enumerate}}

\rub{{Les quatre verdicts (définitions données à l'outil)}}
\begin{{description}}[leftmargin=3.3cm,style=sameline,nosep]
\item[conforme] Le dossier contient un passage qui couvre tout ce que l'exigence demande.
\item[non conforme] Le dossier aborde le sujet, mais il manque une partie de ce que l'exigence demande, ou deux passages se contredisent.
\item[non trouvé] Rien dans le dossier n'aborde le sujet.
\item[non applicable] L'exigence ne vise qu'un cas particulier, et le dossier déclare explicitement que ce cas ne le concerne pas.
  Si le dossier ne dit rien, c'est « non trouvé ».
\end{{description}}
On juge seulement si ce que l'exigence demande est \emph{{présent et cohérent}} dans le dossier, pas si le
contenu technique est exact sur le fond. Si ces définitions vous paraissent mal posées, dites-le à la dernière page.

\rub{{Votre profil (facultatif, pour interpréter vos réponses)}}
Domaine (dispositifs médicaux, DIV, pharmaceutique\ldots) : {line_field("profil_domaine", "6.5cm")}\par
Années d'expérience en affaires réglementaires : {line_field("profil_annees", "3cm")}\par
Avez-vous déjà rédigé ou relu une documentation technique selon l'Annexe II ? \quad
{box("profil_annexe2_oui")}~oui \quad {box("profil_annexe2_non")}~non\par

{{\small\color{{gris}} Texte des exigences : corpus public du projet (\texttt{{corpus/public/mdr/}}, texte consolidé
publié sur EUR-Lex, CELEX 02017R0745-20261109). Outil évalué : modèle ouvert \texttt{{{esc(juge)}}}, campagne du
11 novembre 2026. Aucun nom de personne n'est demandé : ne mettez pas de donnée personnelle dans les remarques.}}
"""


def page_unite(i: int, n: int, req: dict, pred: dict) -> str:
    ctx = req["context"]
    rubrique = first_line(ctx[1]) if len(ctx) > 1 else ""
    parent = ctx[-1].split("\n", 1)[1] if len(ctx) > 2 and "\n" in ctx[-1] else ""
    unit = req["unit"]
    p = [r"\newpage",
         rf"{{\Large\bfseries {i} / {n} \quad \texttt{{{esc(unit)}}}}}\par"]
    if rubrique:
        p.append(rf"{{\small\color{{gris}} Rubrique : {esc(rubrique)}}}\par")
    p.append(r"\rub{L'exigence}")
    p.append(rf"\begin{{quote}}\itshape {esc(req['text'])}\end{{quote}}")
    if parent:
        p.append(rf"{{\small\color{{gris}} Elle complète : « {esc(shorten(parent))} »}}\par")

    v = pred["verdict"]
    p.append(rf"\rub{{La réponse de l'outil : {LIBELLE[v]}}}")
    if pred.get("model_verdict") and pred["model_verdict"] != v:
        p.append(rf"{{\small Le modèle avait proposé « {LIBELLE.get(pred['model_verdict'], pred['model_verdict'])} », "
                 r"mais une de ses citations n'a pas été retrouvée mot pour mot dans le dossier ; "
                 r"par règle, l'outil ramène alors le verdict à « non trouvé ».}\par")
    p.append(rf"\textbf{{Justification :}} {esc(pred.get('rationale', ''))}\par")
    ev = pred.get("evidence") or []
    if ev:
        p.append(r"\textbf{Passages du dossier cités :}")
        p.append(r"\begin{itemize}")
        p += [rf"\item « {esc(e)} »" for e in ev]
        p.append(r"\end{itemize}")
    else:
        p.append(r"\textbf{Passages du dossier cités :} aucun.\par")
    rej = pred.get("rejected_evidence") or []
    if rej:
        p.append(r"{\small\color{gris} Citations non retrouvées mot pour mot (écartées) :}")
        p.append(r"\begin{itemize}\small\color{gris}")
        p += [rf"\item « {esc(e)} »" for e in rej]
        p.append(r"\end{itemize}")

    k = f"u{i}"
    p.append(r"\rub{Vos réponses}")
    p.append(r"\textbf{Q1. Selon vous, le bon verdict est :}\par")
    p.append(rf"{box(k + '_conforme')}~conforme \quad {box(k + '_non_conforme')}~non conforme \quad "
             rf"{box(k + '_non_trouve')}~non trouvé \quad {box(k + '_non_applicable')}~non applicable\par")
    p.append(rf"{box(k + '_indecis')}~je ne peux pas trancher (exigence ou définitions trop floues)\par")
    p.append(r"\textbf{Q2. Les passages cités justifient-ils le verdict de l'outil ?}\par")
    p.append(rf"{box(k + '_cit_oui')}~oui \quad {box(k + '_cit_partiel')}~en partie \quad "
             rf"{box(k + '_cit_non')}~non \quad {box(k + '_cit_sans')}~sans objet (aucun passage cité)\par")
    p.append(r"\textbf{Q3. Votre confiance dans votre réponse à Q1 :}\par")
    p.append(rf"{box(k + '_conf_sure')}~sûre \quad {box(k + '_conf_plutot')}~plutôt sûre \quad "
             rf"{box(k + '_conf_hesitante')}~hésitante\par")
    p.append(r"Remarque (facultatif) : ce qui manque, ce qui vous a fait hésiter, ce qu'un auditeur relèverait\ldots\par")
    p.append(field(k + "_note", "2.2cm"))
    return "\n".join(p)


def fin(n: int) -> str:
    qs = [
        ("g1", r"Entre « non conforme » (le sujet est abordé mais incomplet) et « non trouvé » (rien sur le sujet), "
               r"la frontière vous a-t-elle paru claire ? Que changeriez-vous dans ces définitions ?"),
        ("g2", r"Le verdict « non applicable » n'est accepté que si le dossier déclare explicitement que le cas "
               r"ne le concerne pas. Cette règle vous paraît-elle juste ?"),
        ("g3", r"Le dossier fictif vous paraît-il réaliste ? Qu'est-ce qu'un vrai dossier aurait de plus difficile ?"),
        ("g4", r"Les réponses de l'outil (verdict, citations, justification) vous seraient-elles utiles pour relire "
               r"un vrai dossier ? Qu'est-ce qui manque pour qu'elles le soient ?"),
        ("g5", r"Remarques libres."),
    ]
    p = [r"\newpage", r"{\Large\bfseries Pour finir}\par"]
    for name, q in qs:
        p.append(rf"\rub{{{q}}}")
        p.append(field(name, "2.6cm"))
    p.append(rf"\rub{{Temps passé au total (approximatif)}}{line_field('temps_passe', '4cm')}\par")
    p.append(r"\medskip Merci ! Renvoyez le PDF enregistré. Vos réponses deviendront le corrigé de référence de ce cas "
             r"(après validation par le porteur du projet) et serviront à mesurer l'outil honnêtement.")
    p.append(r"\end{Form}")
    return "\n".join(p)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("case", type=Path)
    ap.add_argument("predictions", type=Path)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--juge", default=None, help="nom du modèle affiché")
    args = ap.parse_args()

    gt = yaml.safe_load((args.case / "ground_truth.yaml").read_text(encoding="utf-8"))
    preds = {}
    for line in args.predictions.read_text(encoding="utf-8").splitlines():
        if line.strip():
            d = json.loads(line)
            preds[d["unit"]] = d
    reqs = {r["unit"]: r for r in requirements_in_scope(load_units(), gt["corpus"]["scope"])}
    order = [u["unit"] for u in gt["units"]]
    missing = [u for u in order if u not in preds or u not in reqs]
    if missing:
        raise SystemExit(f"unités sans prédiction ou absentes du corpus : {missing}")

    juge = args.juge or args.predictions.name.split(".", 1)[1].rsplit(".", 1)[0]
    juge = juge.replace("-", ":", 1) if ":" not in juge and re.search(r"-\d+b$", juge) else juge
    md = (args.case / gt["document"]).read_text(encoding="utf-8")
    n = len(order)
    parts = [PREAMBULE, accueil(gt["case"], n, juge),
             r"\newpage", r"{\Large\bfseries Le dossier fictif à relire}\par",
             r"{\small\color{gris} Dispositif, fabricant et résultats inventés ; lacunes volontaires.}\par\medskip",
             dossier_latex(md)]
    parts += [page_unite(i, n, reqs[u], preds[u]) for i, u in enumerate(order, 1)]
    parts += [fin(n), r"\end{document}", ""]
    tex = "\n".join(parts).replace(f"\\texttt{{{esc(juge)}}}", f"\\texttt{{{esc(juge).replace(':', chr(92) + 'string:')}}}")
    args.out.write_text(tex, encoding="utf-8")
    print(f"{args.out} : {n} exigences, juge {juge}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
