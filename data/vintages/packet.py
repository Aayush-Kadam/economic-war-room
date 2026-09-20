from datetime import datetime
def validate_packet(packet):
    cutoff=datetime.fromisoformat(packet["information_cutoff"])
    if packet.get("actual_policy_action",{}).get("visibility")!="post_commit_only": raise ValueError("historical action must remain hidden")
    suffix=cutoff.strftime("%z"); zone=suffix[:3]+":"+suffix[3:]
    for row in packet["features"]:
        for key in ("series","observation_period","release_date","vintage_date","retrieval_date","transformed_value","source"):
            if key not in row: raise ValueError(f"missing {key}")
        release=datetime.fromisoformat(row["release_date"]+"T00:00:00"+zone); vintage=datetime.fromisoformat(row["vintage_date"]+"T00:00:00"+zone)
        if release>cutoff: raise ValueError("post-cutoff release")
        if vintage>cutoff: raise ValueError("post-cutoff vintage")
