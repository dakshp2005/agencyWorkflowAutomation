"""
Seed script — populates the database with realistic mock data for demo / panelist review.
Run from the agencyWorkflowAutomation/ directory:

    python seed_data.py

The script is idempotent: it checks whether data already exists before inserting,
so it is safe to run multiple times without duplication.
"""

import sys
import os
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(__file__))

from app import create_app
from app.config import DevelopmentConfig
from app.extensions import db
from app.models.client import Client
from app.models.email_record import EmailRecord
from app.models.reply import InboundReply
from app.models.meeting import Meeting
from app.models.interaction_log import InteractionLog
from app.models.notification import Notification

app = create_app(DevelopmentConfig)

# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def dt(days_ago: int, hour: int = 10, minute: int = 0) -> datetime:
    """Return a datetime offset from today."""
    return datetime.utcnow() - timedelta(days=days_ago, hours=0) + timedelta(hours=hour - 10, minutes=minute)


# ---------------------------------------------------------------------------
# Mock data definitions
# ---------------------------------------------------------------------------

CLIENTS = [
    dict(
        name="Sarah Chen",
        email="sarah.chen@technovasolutions.com",
        company="TechNova Solutions",
        industry="Software / SaaS",
        website="https://technovasolutions.com",
        phone="+1-415-555-0192",
        preferences="Prefers concise proposals, interested in AI-powered automation, budget ~$40k",
        notes="Referred by existing client. Very responsive. Decision-maker.",
        status="converted",
    ),
    dict(
        name="Marcus Rodriguez",
        email="marcus.r@greenpath.io",
        company="GreenPath Consulting",
        industry="Sustainability / ESG",
        website="https://greenpath.io",
        phone="+1-312-555-0847",
        preferences="Values sustainability angle in proposals, prefers Slack over email, timeline flexibility",
        notes="Engaged during webinar. Mid-size team, open to multi-phase rollout.",
        status="proposal_sent",
    ),
    dict(
        name="Priya Patel",
        email="priya.patel@healthfirst.med",
        company="HealthFirst Innovations",
        industry="Healthcare Technology",
        website="https://healthfirst.med",
        phone="+1-617-555-0334",
        preferences="Requires HIPAA compliance mention, needs detailed timeline, formal tone",
        notes="Procurement committee involved. Expect 2-3 week decision cycle.",
        status="meeting_scheduled",
    ),
    dict(
        name="David Kim",
        email="d.kim@retailedge.co",
        company="RetailEdge Inc",
        industry="Retail / E-commerce",
        website="https://retailedge.co",
        phone="+1-213-555-0561",
        preferences="Focus on ROI metrics, wants case studies, budget TBD",
        notes="Comparing three agencies. Key concern: integration with Shopify stack.",
        status="replied",
    ),
    dict(
        name="Amanda Foster",
        email="amanda@brightbrandagency.com",
        company="BrightBrand Agency",
        industry="Marketing & Advertising",
        website="https://brightbrandagency.com",
        phone="+1-212-555-0728",
        preferences="Creative-first approach, short turnaround, open to performance-based pricing",
        notes="Warm lead from LinkedIn. Looking to outsource workflow ops.",
        status="outreach_sent",
    ),
    dict(
        name="James Okafor",
        email="james.okafor@financeforward.ng",
        company="FinanceForward",
        industry="FinTech",
        website="https://financeforward.ng",
        phone="+234-801-555-0090",
        preferences="Needs compliance documentation, interested in data security practices",
        notes="Lost deal — budget freeze. Keep warm for Q3 revisit.",
        status="not_interested",
    ),
]

# (client_email, subject, body, email_type, status, days_ago)
EMAILS = [
    (
        "sarah.chen@technovasolutions.com",
        "Introducing Agency Automation Solutions for TechNova",
        """Hi Sarah,

I hope this finds you well. I'm reaching out because TechNova Solutions caught our eye — the work you're doing in the SaaS space is impressive, and we believe we can help you scale your client workflows significantly.

Our agency has helped similar software companies reduce manual outreach effort by 60% and cut proposal turnaround from days to hours.

Would you be open to a 20-minute call this week to explore the fit?

Best,
The Agency Team""",
        "outreach", "sent", 14,
    ),
    (
        "sarah.chen@technovasolutions.com",
        "Re: Proposal for TechNova Solutions — follow-up",
        """Hi Sarah,

Following up on the proposal we sent over last week. I wanted to check whether you had a chance to review it and address any questions.

We're flexible on the timeline and happy to adjust the scope if needed.

Looking forward to hearing from you!""",
        "followup", "sent", 7,
    ),
    (
        "marcus.r@greenpath.io",
        "Sustainability-Focused Workflow Automation for GreenPath",
        """Hi Marcus,

Great connecting at the ESG webinar last month! As promised, I'm sending over our tailored overview for GreenPath.

We've worked with three sustainability consultancies this year, helping them automate client onboarding and proposal generation — all while aligning communications with their brand values.

Would love to walk you through a short demo. Are you available for a call this week?""",
        "outreach", "sent", 18,
    ),
    (
        "priya.patel@healthfirst.med",
        "HIPAA-Compliant Automation Proposal for HealthFirst Innovations",
        """Dear Priya,

Thank you for your time on our discovery call earlier this month. As discussed, I'm pleased to share our formal proposal for HealthFirst Innovations.

All our workflows are designed with HIPAA compliance in mind, and we include a full data handling addendum upon contract signing.

Please find the proposal attached. I'm available for a review session at your convenience.

Warm regards,
The Agency Team""",
        "outreach", "sent", 10,
    ),
    (
        "d.kim@retailedge.co",
        "Agency Automation — Shopify Integration Case Study for RetailEdge",
        """Hi David,

Per our chat, I'm sharing a case study from a comparable retail client where we achieved 3x faster proposal turnaround and a 45% improvement in reply-to-meeting conversion.

Our Shopify-native integration means zero disruption to your existing stack.

Would a 30-minute walkthrough work for you next Tuesday?""",
        "outreach", "sent", 9,
    ),
    (
        "amanda@brightbrandagency.com",
        "Let's Automate BrightBrand's Client Workflow",
        """Hi Amanda,

Loved your recent campaign work for the fashion vertical — very sharp positioning!

We help agencies like BrightBrand cut the admin overhead of client onboarding, follow-ups, and proposal generation so your team can focus on creative work.

Happy to share a performance-based pricing model that aligns our success with yours.

Open to a quick chat?""",
        "outreach", "sent", 6,
    ),
    (
        "james.okafor@financeforward.ng",
        "FinTech-Ready Workflow Automation for FinanceForward",
        """Hi James,

Following your enquiry, I've put together a brief overview of how our platform handles compliance documentation and audit trails — both critical for FinTech operations.

We're happy to sign an NDA before sharing the detailed architecture.

Let me know if this is still on your radar.""",
        "outreach", "sent", 21,
    ),
]

# (client_email, sender_email, subject, raw_body, classification, extracted_entities, action_taken, days_ago, hour)
REPLIES = [
    (
        "sarah.chen@technovasolutions.com",
        "sarah.chen@technovasolutions.com",
        "Re: Introducing Agency Automation Solutions for TechNova",
        """Hi,

Thank you for reaching out! We've been looking for exactly this kind of solution. The AI-powered proposal generation especially caught our attention.

Can we schedule a call on March 10th at 2 PM PST or March 11th at 10 AM PST?

Also, do you have references from other SaaS companies we could speak with?

Best,
Sarah Chen
VP of Operations, TechNova Solutions""",
        "POSITIVE",
        {"dates": ["March 10th at 2 PM PST", "March 11th at 10 AM PST"], "companies": ["TechNova Solutions"], "requirements": ["AI-powered proposals", "SaaS references"]},
        "meeting_proposed",
        13, 14,
    ),
    (
        "sarah.chen@technovasolutions.com",
        "sarah.chen@technovasolutions.com",
        "Re: Proposal for TechNova Solutions — follow-up",
        """Hi team,

We reviewed the proposal with our CTO and we're ready to move forward. The scope looks right and the pricing is within our budget.

Can we set up a kick-off call for the week of March 15th? Preferred time is morning slots.

Looking forward to working together!

Sarah""",
        "POSITIVE",
        {"dates": ["week of March 15th"], "companies": ["TechNova Solutions"], "requirements": ["kick-off call", "morning slots"]},
        "meeting_confirmed",
        6, 11,
    ),
    (
        "marcus.r@greenpath.io",
        "marcus.r@greenpath.io",
        "Re: Sustainability-Focused Workflow Automation for GreenPath",
        """Hi,

The proposal looks solid. A couple of clarifications before we proceed:

1. Can you detail how the AI ensures brand tone consistency for sustainability messaging?
2. What's the typical implementation timeline for a 15-person team?
3. Do you offer a pilot engagement before a full rollout?

We have a board review on March 20th and would love to present this as a potential initiative.

Marcus""",
        "NEUTRAL",
        {"dates": ["March 20th"], "companies": ["GreenPath Consulting"], "requirements": ["brand tone AI", "implementation timeline", "pilot engagement", "15-person team"]},
        "reply_logged",
        15, 16,
    ),
    (
        "priya.patel@healthfirst.med",
        "priya.patel@healthfirst.med",
        "Re: HIPAA-Compliant Automation Proposal for HealthFirst Innovations",
        """Dear Team,

Thank you for the detailed proposal. Our compliance officer has reviewed the data handling section and has a few questions:

- Is your infrastructure SOC 2 Type II certified?
- Can you provide the data residency documentation for US-based storage?
- The timeline mentions 6 weeks — is this negotiable to 4 weeks?

We have a procurement meeting scheduled for March 18th, after which we expect to make a decision.

Best regards,
Priya Patel
Head of Digital, HealthFirst Innovations""",
        "NEUTRAL",
        {"dates": ["March 18th"], "companies": ["HealthFirst Innovations"], "requirements": ["SOC 2 Type II", "data residency", "4-week timeline", "HIPAA"]},
        "reply_logged",
        8, 9,
    ),
    (
        "d.kim@retailedge.co",
        "d.kim@retailedge.co",
        "Re: Agency Automation — Shopify Integration Case Study for RetailEdge",
        """Hi,

Thanks for the case study — impressive numbers! We're currently evaluating two other vendors as well.

A few things would help us decide:
- Can you demo the Shopify connector live?
- What's the contract minimum commitment period?
- Do you offer white-label reporting?

We plan to finalize our vendor selection by end of March.

David Kim
CTO, RetailEdge Inc""",
        "NEUTRAL",
        {"dates": ["end of March"], "companies": ["RetailEdge Inc"], "requirements": ["Shopify demo", "contract commitment", "white-label reporting"]},
        "reply_logged",
        7, 15,
    ),
    (
        "amanda@brightbrandagency.com",
        "amanda@brightbrandagency.com",
        "Re: Let's Automate BrightBrand's Client Workflow",
        """Hi,

Appreciate you reaching out. We actually just signed with another automation vendor last week after a long evaluation process.

We may revisit in Q4 if circumstances change. Feel free to check back then.

Thanks,
Amanda Foster""",
        "NEGATIVE",
        {"dates": ["Q4"], "companies": ["BrightBrand Agency"], "requirements": []},
        "marked_not_interested",
        4, 10,
    ),
    (
        "james.okafor@financeforward.ng",
        "james.okafor@financeforward.ng",
        "Re: FinTech-Ready Workflow Automation for FinanceForward",
        """Hello,

Thank you for the detailed overview. Unfortunately, we've had to freeze all non-critical vendor expenditures for Q1 and Q2 due to a regulatory audit we're currently undergoing.

This is not a reflection on your offering — we were genuinely impressed. We'd like to reconnect in Q3 when the budget cycle resets.

James Okafor
CEO, FinanceForward""",
        "NEGATIVE",
        {"dates": ["Q3"], "companies": ["FinanceForward"], "requirements": ["budget freeze", "regulatory audit"]},
        "marked_not_interested",
        19, 13,
    ),
]

# (client_email, proposed_slots, confirmed_slot, agenda, status, days_ago_created)
MEETINGS = [
    (
        "sarah.chen@technovasolutions.com",
        ["2026-03-10T14:00:00", "2026-03-11T10:00:00", "2026-03-12T15:00:00"],
        "2026-03-11T10:00:00",
        "Kick-off call: project scope confirmation, team introductions, onboarding checklist walkthrough, Q&A.",
        "confirmed",
        12,
    ),
    (
        "priya.patel@healthfirst.med",
        ["2026-03-18T09:00:00", "2026-03-19T14:00:00", "2026-03-20T11:00:00"],
        None,
        "Compliance review Q&A, SOC 2 documentation walkthrough, finalise timeline and procurement steps.",
        "proposed",
        7,
    ),
    (
        "marcus.r@greenpath.io",
        ["2026-03-17T10:00:00", "2026-03-18T15:00:00"],
        "2026-03-17T10:00:00",
        "Pilot scope discussion, brand tone AI demo, rollout timeline for 15-person team, board presentation prep.",
        "confirmed",
        10,
    ),
    (
        "d.kim@retailedge.co",
        ["2026-03-25T13:00:00", "2026-03-26T10:00:00"],
        None,
        "Live Shopify connector demo, white-label reporting walkthrough, commercial terms review.",
        "proposed",
        5,
    ),
]


# ---------------------------------------------------------------------------
# Seeding logic
# ---------------------------------------------------------------------------

def seed():
    with app.app_context():
        # Guard: skip if replies already exist
        if InboundReply.query.count() > 0:
            print("Database already seeded (replies found). Skipping.")
            return

        print("Seeding clients...")
        client_map = {}  # email -> Client instance
        for c in CLIENTS:
            existing = Client.query.filter_by(email=c["email"]).first()
            if existing:
                client_map[c["email"]] = existing
            else:
                obj = Client(**c)
                db.session.add(obj)
                db.session.flush()
                client_map[c["email"]] = obj
        db.session.commit()
        print(f"  {len(client_map)} clients ready.")

        print("Seeding emails...")
        for (c_email, subject, body, e_type, status, days_ago) in EMAILS:
            client = client_map.get(c_email)
            if not client:
                continue
            em = EmailRecord(
                client_id=client.id,
                subject=subject,
                body=body,
                email_type=e_type,
                status=status,
                sent_at=dt(days_ago, hour=9),
                created_at=dt(days_ago + 1, hour=8),
            )
            db.session.add(em)
        db.session.commit()
        print(f"  {len(EMAILS)} emails seeded.")

        print("Seeding inbound replies...")
        for (c_email, sender, subject, body, classification, entities, action, days_ago, hour) in REPLIES:
            client = client_map.get(c_email)
            reply = InboundReply(
                client_id=client.id if client else None,
                sender_email=sender,
                subject=subject,
                raw_body=body,
                classification=classification,
                extracted_entities=entities,
                action_taken=action,
                processed_at=dt(days_ago, hour=hour),
            )
            db.session.add(reply)

            # Update client status based on reply classification
            if client:
                if classification == "NEGATIVE":
                    client.status = "not_interested"
                elif classification == "POSITIVE" and client.status not in ("converted",):
                    client.status = "replied"
                elif classification == "NEUTRAL" and client.status == "outreach_sent":
                    client.status = "replied"

        db.session.commit()
        print(f"  {len(REPLIES)} replies seeded.")

        print("Seeding meetings...")
        for (c_email, slots, confirmed, agenda, status, days_ago) in MEETINGS:
            client = client_map.get(c_email)
            if not client:
                continue
            mtg = Meeting(
                client_id=client.id,
                proposed_slots=slots,
                confirmed_slot=confirmed,
                agenda=agenda,
                status=status,
                created_at=dt(days_ago, hour=11),
            )
            db.session.add(mtg)
            if status == "confirmed":
                client.status = "meeting_scheduled"
        db.session.commit()
        print(f"  {len(MEETINGS)} meetings seeded.")

        print("Seeding interaction logs...")
        logs = [
            # Sarah Chen — full journey
            ("sarah.chen@technovasolutions.com", "email_generated",  "Outreach email drafted for Sarah Chen at TechNova Solutions", 14),
            ("sarah.chen@technovasolutions.com", "email_sent",       "Outreach email sent to sarah.chen@technovasolutions.com", 14),
            ("sarah.chen@technovasolutions.com", "reply_classified",  "Reply classified as POSITIVE — meeting slots proposed by client", 13),
            ("sarah.chen@technovasolutions.com", "meeting_proposed",  "Meeting proposed: 3 slots offered for kick-off call", 13),
            ("sarah.chen@technovasolutions.com", "email_sent",       "Follow-up email sent to Sarah Chen", 7),
            ("sarah.chen@technovasolutions.com", "reply_classified",  "Second reply classified as POSITIVE — client confirmed readiness to proceed", 6),
            ("sarah.chen@technovasolutions.com", "meeting_confirmed", "Kick-off meeting confirmed for March 11 at 10:00 AM PST", 6),
            ("sarah.chen@technovasolutions.com", "document_generated","Proposal generated: Proposal for TechNova Solutions", 5),
            ("sarah.chen@technovasolutions.com", "approval_granted",  "Proposal approved and marked for delivery", 4),

            # Marcus Rodriguez
            ("marcus.r@greenpath.io", "email_generated",  "Outreach email drafted for Marcus Rodriguez at GreenPath Consulting", 18),
            ("marcus.r@greenpath.io", "email_sent",       "Outreach email sent to marcus.r@greenpath.io", 18),
            ("marcus.r@greenpath.io", "reply_classified",  "Reply classified as NEUTRAL — client asked clarification questions", 15),
            ("marcus.r@greenpath.io", "meeting_proposed",  "Discovery call proposed to address GreenPath clarifications", 14),
            ("marcus.r@greenpath.io", "meeting_confirmed", "Meeting confirmed: March 17 pilot scope discussion", 10),
            ("marcus.r@greenpath.io", "document_generated","Proposal generated for GreenPath Consulting", 8),
            ("marcus.r@greenpath.io", "approval_requested","Proposal submitted for internal approval", 8),

            # Priya Patel
            ("priya.patel@healthfirst.med", "email_generated",  "Outreach email drafted for Priya Patel at HealthFirst Innovations", 11),
            ("priya.patel@healthfirst.med", "email_sent",       "Outreach email sent to priya.patel@healthfirst.med", 10),
            ("priya.patel@healthfirst.med", "reply_classified",  "Reply classified as NEUTRAL — compliance questions raised", 8),
            ("priya.patel@healthfirst.med", "meeting_proposed",  "Meeting proposed to address HIPAA/SOC 2 compliance queries", 7),

            # David Kim
            ("d.kim@retailedge.co", "email_generated",  "Outreach email drafted for David Kim at RetailEdge Inc", 10),
            ("d.kim@retailedge.co", "email_sent",       "Outreach email sent to d.kim@retailedge.co", 9),
            ("d.kim@retailedge.co", "reply_classified",  "Reply classified as NEUTRAL — evaluation in progress, demo requested", 7),
            ("d.kim@retailedge.co", "meeting_proposed",  "Live demo session proposed for Shopify connector", 5),

            # Amanda Foster
            ("amanda@brightbrandagency.com", "email_generated",  "Outreach email drafted for Amanda Foster at BrightBrand Agency", 7),
            ("amanda@brightbrandagency.com", "email_sent",       "Outreach email sent to amanda@brightbrandagency.com", 6),
            ("amanda@brightbrandagency.com", "reply_classified",  "Reply classified as NEGATIVE — client selected competing vendor", 4),

            # James Okafor
            ("james.okafor@financeforward.ng", "email_generated",  "Outreach email drafted for James Okafor at FinanceForward", 22),
            ("james.okafor@financeforward.ng", "email_sent",       "Outreach email sent to james.okafor@financeforward.ng", 21),
            ("james.okafor@financeforward.ng", "reply_classified",  "Reply classified as NEGATIVE — budget freeze due to regulatory audit", 19),
        ]

        for (c_email, action_type, description, days_ago) in logs:
            client = client_map.get(c_email)
            log = InteractionLog(
                client_id=client.id if client else None,
                action_type=action_type,
                description=description,
                timestamp=dt(days_ago, hour=10),
            )
            db.session.add(log)
        db.session.commit()
        print(f"  {len(logs)} interaction log entries seeded.")

        print("Seeding notifications...")
        notifications = [
            dict(
                title="Proposal Approval Required — TechNova Solutions",
                message="A new proposal has been generated for Sarah Chen (TechNova Solutions) and requires your approval before delivery.",
                notification_type="document_approval",
                is_read=True,
                action_url="/documents/",
                created_at=dt(5, hour=10),
            ),
            dict(
                title="Proposal Approval Required — GreenPath Consulting",
                message="A new proposal has been generated for Marcus Rodriguez (GreenPath Consulting) and is pending approval.",
                notification_type="document_approval",
                is_read=False,
                action_url="/documents/",
                created_at=dt(8, hour=11),
            ),
            dict(
                title="Meeting Confirmed — TechNova Solutions Kick-off",
                message="Sarah Chen confirmed the kick-off meeting for March 11 at 10:00 AM PST.",
                notification_type="meeting_created",
                is_read=True,
                action_url="/meetings/",
                created_at=dt(6, hour=12),
            ),
            dict(
                title="New Reply — HealthFirst Innovations",
                message="Priya Patel replied with compliance questions. Review and prepare SOC 2 documentation.",
                notification_type="reply_received",
                is_read=False,
                action_url="/replies/",
                created_at=dt(8, hour=9),
            ),
            dict(
                title="New Reply — RetailEdge Inc",
                message="David Kim requested a live Shopify demo. Schedule a demo session.",
                notification_type="reply_received",
                is_read=False,
                action_url="/replies/",
                created_at=dt(7, hour=15),
            ),
            dict(
                title="Negative Reply — BrightBrand Agency",
                message="Amanda Foster declined — client selected a competing vendor. Status updated to Not Interested.",
                notification_type="reply_received",
                is_read=True,
                action_url="/replies/",
                created_at=dt(4, hour=10),
            ),
            dict(
                title="Outreach Email Approval Required — Amanda Foster",
                message="An outreach email for Amanda Foster (BrightBrand Agency) is awaiting your approval.",
                notification_type="email_approval",
                is_read=True,
                action_url="/emails/",
                created_at=dt(7, hour=8),
            ),
        ]

        for n in notifications:
            notif = Notification(**n)
            db.session.add(notif)
        db.session.commit()
        print(f"  {len(notifications)} notifications seeded.")

        print("\n✅ Seed complete! Summary:")
        print(f"   Clients      : {Client.query.count()}")
        print(f"   Emails       : {EmailRecord.query.count()}")
        print(f"   Replies      : {InboundReply.query.count()}")
        print(f"   Meetings     : {Meeting.query.count()}")
        print(f"   Activity Logs: {InteractionLog.query.count()}")
        print(f"   Notifications: {Notification.query.count()}")


if __name__ == "__main__":
    seed()
