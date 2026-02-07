#!/usr/bin/env bash
# mkdir_tree.sh — Create the full worldtree directory skeleton
ROOT="${WORLDROOT:-worldtree.root.window/jiadongchendonnie.ai}"

mkdir -p "$ROOT"/projects/JCD01-evidence-vault/{evidence/{originals,derivatives},meta,provenance,integrity,exports}
mkdir -p "$ROOT"/projects/JCD02-os-remap-library/{mappings,rules,samples,tests}
mkdir -p "$ROOT"/projects/JCD03-privacy-boundary-policy-engine/{policies,modes,alignments,enforcement,audit}
mkdir -p "$ROOT"/projects/JCD04-au-legal-atlas-online-data/{commonwealth/{legislation-primary,regulators-guidance},states-territories,references}
mkdir -p "$ROOT"/projects/JCD05-canberra-contact-router/{parliament,prime-minister,regulators,directory}
mkdir -p "$ROOT"/projects/JCD06-device-event-timeline/{nodes,timelines,device-state,app-data,bundles}

mkdir -p "$ROOT"/schemas/{node-timestamp,os-sample,evidence,conversation-record}
mkdir -p "$ROOT"/samples/{os,templates,conversation}

mkdir -p "$ROOT"/conservations/local/{raw,normalized,indexes,attachments,redactions,provenance,exports}
mkdir -p "$ROOT"/conservations/shared-links/{raw,snapshots,normalized,provenance}
mkdir -p "$ROOT"/conservations/memory-layer/{raw,versions,audit}
mkdir -p "$ROOT"/conservations/logs/{ingest,remap,export}

mkdir -p "$ROOT"/external-conservations/imports/{raw,manifests,provenance}
mkdir -p "$ROOT"/external-conservations/sources/{chatgpt,email,imessage,whatsapp,wechat,telegram,slack,discord,box,dropbox,other}
mkdir -p "$ROOT"/external-conservations/normalized/{nodes,threads,attachments}
mkdir -p "$ROOT"/external-conservations/os-samples/{raw,mapped,tests}
mkdir -p "$ROOT"/external-conservations/{redactions,indexes,exports}

mkdir -p "$ROOT"/connectors/{slack,box,dropbox}/{cache,scripts}
mkdir -p "$ROOT"/scripts
mkdir -p "$ROOT"/projects/JCD01-evidence-vault/integrity/manifests-signatures
mkdir -p "$ROOT"/projects/JCD01-evidence-vault/integrity/merkle-roots

echo "Created worldtree at: $ROOT"
