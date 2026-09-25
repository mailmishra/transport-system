"""Realistic, stress-testing demo data for local development.

Gated by SEED_DEMO_DATA (Settings.seed_demo_data): true only in the local
docker-compose environment (see docker-compose.yml), unset -- so False --
on Railway/production (railway.json sets no such variable). Idempotent:
skips entirely if a Bilti with the MARKER_PREFIX below already exists, so
re-running `docker compose up` never duplicates data.

Run via `python -m app.scripts.seed_demo_data` (see backend/Dockerfile's
CMD, chained with `|| true` so a seeding failure can never block the app
from starting).

Uses Starlette's TestClient against the real `app` object -- the same
pattern backend/tests/conftest.py uses -- so every record goes through the
actual API's Pydantic validation and get-or-create CRUD logic, not a raw
DB insert. If a call fails, it's logged and skipped rather than crashing
the whole run, so a partial seed is still useful data to look at.

This is deliberately NOT a happy-path-only fixture. It's built to exercise
the same edge cases integration tests check for, but as data a human can
click through in the UI: optional fields left blank, get-or-create name
normalization (case/whitespace), soft deletes, over-payments, over-receipts,
a firm with no letterhead, a firm with zero activity, unicode party names,
near-max-length text, and enough rows on Bilti to cross a pagination page
boundary. See the section comments below for what each block is proving.
"""
from __future__ import annotations

from datetime import date, timedelta

from starlette.testclient import TestClient

from app.config import get_settings
from app.main import app

MARKER_PREFIX = "DEMO-GR-"


def log(msg: str) -> None:
    print(f"[seed_demo_data] {msg}", flush=True)


def d(days_ago: int) -> str:
    return (date.today() - timedelta(days=days_ago)).isoformat()


def post(client: TestClient, path: str, payload: dict, *, label: str) -> dict | None:
    res = client.post(path, json=payload)
    if res.status_code not in (200, 201):
        log(f"WARN: {label} failed ({res.status_code}): {res.text[:300]}")
        return None
    return res.json()


def patch(client: TestClient, path: str, payload: dict, *, label: str) -> dict | None:
    res = client.patch(path, json=payload)
    if res.status_code != 200:
        log(f"WARN: {label} failed ({res.status_code}): {res.text[:300]}")
        return None
    return res.json()


def delete(client: TestClient, path: str, *, label: str) -> bool:
    res = client.delete(path)
    if res.status_code != 204:
        log(f"WARN: {label} failed ({res.status_code}): {res.text[:300]}")
        return False
    return True


def main() -> None:
    settings = get_settings()
    if not settings.seed_demo_data:
        log("SEED_DEMO_DATA is off -- skipping (expected on Railway/production).")
        return

    with TestClient(app, base_url="http://seed") as client:
        firms = client.get("/api/firms").json()
        if not firms:
            log("WARN: no firms found (migration 0001 should have seeded 3) -- aborting.")
            return
        firm_by_name = {f["name"]: f for f in firms}
        firm = firm_by_name.get("Shivam Transport Company", firms[0])
        firm_id = firm["id"]

        already = client.get("/api/bilties", params={"q": MARKER_PREFIX, "limit": 1}).json()
        if already["total"] > 0:
            log(f"Demo data already present (found a '{MARKER_PREFIX}*' Bilti) -- skipping.")
            return

        log(f"Seeding demo data into '{firm['name']}' ({firm_id})...")

        # -- Firm letterhead: primary firm gets full bank/letterhead details
        # (exercises the print view's bank-details footer + PAN line). A
        # second firm is deliberately left blank (tests the print view's
        # conditional omission of that footer) -- see firm_2 below. The
        # third seeded firm ("Sri Krishna Transport Company") is untouched
        # entirely: a zero-activity firm, useful for checking empty states
        # once a firm switcher exists (AppShell currently hardcodes
        # firms[0], so it won't surface in the UI today, but the data is
        # there for when it does).
        patch(
            client,
            f"/api/firms/{firm_id}",
            {
                "address": "142 Station Road, Indore, Madhya Pradesh 452001",
                "phone": "+91 98765 43210",
                "email": "accounts@shivamtransport.example",
                "pan_no": "AABCS1234D",
                "bank_name": "State Bank of India",
                "bank_branch": "Indore Main Branch",
                "bank_account_no": "32456789012",
                "bank_ifsc": "SBIN0001234",
            },
            label="firm letterhead",
        )
        firm_2 = firm_by_name.get("Shivsakti Transport Company")
        firm_2_id = firm_2["id"] if firm_2 else None

        # ------------------------------------------------------------------
        # Loading Slips (~14). Varied optional-field combinations: with/
        # without truck owner & agent, advance_amount = 0 (print view must
        # omit the "Advance:" line), advance_note without an advance
        # figure, missing package_count (Hindi sentence falls back to "—"),
        # and unicode destinations.
        # ------------------------------------------------------------------
        def loading_slip(**over: object) -> dict | None:
            payload = {
                "firm_id": firm_id,
                "slip_date": d(20),
                "vehicle_no": "MP09XY1234",
                "truck_owner_name": "Ramesh Singh Transport",
                "agent_name": "Suresh Bhai",
                "loading_point": "Indore",
                "destination": "Bhopal",
                "goods_description": "Cotton Bales",
                "quantity_weight": "5000 kg",
                "package_count": "200 bags",
                "advance_amount": 1000,
                "advance_note": "Cash advance at loading point",
            }
            payload.update(over)
            return post(client, "/api/loading-slips", payload, label=f"loading-slip {payload.get('vehicle_no')}")

        ls_linked = loading_slip(
            slip_date=d(25),
            vehicle_no="RJ14GB5678",
            truck_owner_name="Gupta Carriers",
            agent_name="Mahesh Traders",
            loading_point="Ratlam",
            destination="Jabalpur",
            goods_description="Cement Bags",
            quantity_weight="5750 kg",
            package_count="150 bags",
            advance_amount=3000,
            advance_note="Cash advance at loading point",
            factory_name="Narmada Cement Mill",
        )
        loading_slip(  # no truck owner, no agent -- both are optional
            slip_date=d(19),
            vehicle_no="GJ05CT4321",
            truck_owner_name=None,
            agent_name=None,
            loading_point="Vadodara",
            destination="Surat",
            goods_description="Textile Rolls",
            quantity_weight="3200 kg",
            package_count=None,
            advance_amount=0,
            advance_note=None,
        )
        loading_slip(  # factory_name set, advance_amount=0 with a note
            slip_date=d(18),
            vehicle_no="UP32AB9999",
            truck_owner_name="Gupta Carriers",
            agent_name=None,
            loading_point="Lucknow",
            destination="Kanpur",
            goods_description="Steel Rods",
            quantity_weight="12000 kg",
            package_count="80 bundles",
            advance_amount=0,
            advance_note="Advance to be settled on delivery, not at loading",
            factory_name="Kanpur Steel Works",
        )
        loading_slip(
            slip_date=d(17),
            vehicle_no="MH12CD3456",
            truck_owner_name="Bhopal Freight Carriers",
            agent_name="Om Logistics Agency",
            loading_point="भोपाल",
            destination="इंदौर",
            goods_description="चावल की बोरियां (Rice Sacks)",
            quantity_weight="6000 kg",
            package_count="300 बोरी",
            advance_amount=1500,
        )
        for i in range(9):
            loading_slip(
                slip_date=d(16 - i),
                vehicle_no=["MP09XY1234", "RJ14GB5678", "GJ05CT4321", "CG04EF7890"][i % 4],
                truck_owner_name=["Ramesh Singh Transport", "Patel Roadways", "Gupta Carriers"][i % 3],
                agent_name="Suresh Bhai" if i % 2 == 0 else None,
                loading_point=["Indore", "Ratlam", "Dewas", "Ujjain"][i % 4],
                destination=["Bhopal", "Jabalpur", "Gwalior", "Sagar"][i % 4],
                goods_description=["Cotton Bales", "Cement Bags", "Wheat Grain", "Auto Parts"][i % 4],
                quantity_weight=f"{4000 + i * 350} kg",
                package_count=f"{100 + i * 10} bags",
                advance_amount=500 * (i % 5),
            )

        # ------------------------------------------------------------------
        # Bilties (~24, including one soft-deleted). This is the core
        # stress pass -- see inline comments per record for what each one
        # is proving. Enough volume to cross the Bilti list's default
        # page-1/limit-20 boundary.
        # ------------------------------------------------------------------
        def mk_bilti(**over: object) -> dict:
            payload = {
                "firm_id": firm_id,
                "bilti_date": d(15),
                "consignor": "Default Consignor",
                "consignee": "Default Consignee",
                "from_location": "Indore",
                "to_location": "Bhopal",
                "vehicle_no": "MP09XY1234",
                "truck_owner_name": "Ramesh Singh Transport",
                "goods_description": "General Goods",
                "weight": "5000 kg",
                "freight": 5000,
            }
            payload.update(over)
            return payload

        bilties: dict[str, dict] = {}

        def create_bilti(tag: str, **over: object) -> None:
            payload = mk_bilti(**over)
            result = post(client, "/api/bilties", payload, label=f"bilti {payload['bilti_no']}")
            if result:
                bilties[tag] = result

        n = 1

        def next_no() -> str:
            nonlocal n
            no = f"{MARKER_PREFIX}{n:03d}"
            n += 1
            return no

        # 1. Full happy path: every optional field populated, insured,
        #    all charge fields nonzero, all compliance fields set.
        create_bilti(
            "full_happy_path",
            bilti_no=next_no(),
            bilti_date=d(30),
            consignor="Ganesh Traders Pvt Ltd",
            consignee="Sunrise Wholesale Mart",
            from_location="Indore",
            to_location="Mumbai",
            vehicle_no="MP09XY1234",
            palti_vehicle_no="MH12CD3456",
            truck_owner_name="Ramesh Singh Transport",
            agent_name="Suresh Bhai",
            goods_description="Electronics - Consumer Appliances",
            weight="8200 kg",
            charged_weight="8500 kg",
            package_count="340",
            package_unit="BOX",
            freight_rate=1.85,
            freight=15170,
            dalali=600,
            advance_to_owner=5000,
            freight_difference=250,
            other_charges=200,
            kanta_charges=100,
            bahi_charges=50,
            service_tax=150,
            hamali=400,
            p_freight=0,
            gst_paid_by="consignor",
            eway_bill_no="EWB240912345678",
            invoice_value=450000,
            insured=True,
            insurance_company="National Insurance Co.",
            insurance_policy_no="NIC/2026/883210",
            insurance_amount=450000,
            insurance_date=d(31),
            insurance_risk="Transit — Fire & Theft",
            insurance_agent_name="Rakesh Insurance Agency",
            goods_value_declared=450000,
            remark="Handle with care — fragile electronics, no stacking above 2 pallets.",
        )

        # 2. Bare-minimum required fields only -- every optional field
        #    omitted. Print view / list must render blanks gracefully.
        create_bilti(
            "bare_minimum",
            bilti_no=next_no(),
            bilti_date=d(29),
            consignor="Local Kirana Store",
            consignee="Rural Distribution Point",
            from_location="Dewas",
            to_location="Ujjain",
            vehicle_no="GJ05CT4321",
            truck_owner_name="Gupta Carriers",
            agent_name="Suresh Bhai",
            goods_description="Groceries",
            weight="1200 kg",
            freight=2200,
        )

        # 3/4. Same agent ("Suresh Bhai") on two more bilties with
        #    non-zero dalali+FD -- feeds a normal, underpaid Agent Ledger
        #    balance once a partial payment is recorded below.
        create_bilti(
            "agent_a_1",
            bilti_no=next_no(),
            bilti_date=d(28),
            consignor="Malwa Agro Traders",
            consignee="Central Warehouse Corp",
            vehicle_no="RJ14GB5678",
            truck_owner_name="Patel Roadways",
            agent_name="Suresh Bhai",
            goods_description="Soybean Sacks",
            weight="10000 kg",
            freight=18000,
            dalali=700,
            freight_difference=300,
            advance_to_owner=6000,
        )
        create_bilti(
            "agent_a_2",
            bilti_no=next_no(),
            bilti_date=d(24),
            consignor="Malwa Agro Traders",
            consignee="Eastern Grain Depot",
            vehicle_no="RJ14GB5678",
            truck_owner_name="Patel Roadways",
            agent_name="Suresh Bhai",
            goods_description="Soybean Sacks",
            weight="9800 kg",
            freight=17500,
            dalali=650,
            freight_difference=0,
            advance_to_owner=5500,
        )

        # 5/6. "Mahesh Traders" -- will be OVER-paid below (balance goes
        #    negative). Proves the UI doesn't choke on a negative balance.
        create_bilti(
            "agent_b_1",
            bilti_no=next_no(),
            bilti_date=d(27),
            consignor="Vindhya Steel Corp",
            consignee="Metro Hardware Ltd",
            vehicle_no="UP32AB9999",
            truck_owner_name="Bhopal Freight Carriers",
            agent_name="Mahesh Traders",
            goods_description="Steel Rods",
            weight="15000 kg",
            freight=22000,
            dalali=400,
            freight_difference=100,
        )
        create_bilti(
            "agent_b_2",
            bilti_no=next_no(),
            bilti_date=d(22),
            consignor="Vindhya Steel Corp",
            consignee="Northern Fabricators",
            vehicle_no="UP32AB9999",
            truck_owner_name="Bhopal Freight Carriers",
            agent_name="Mahesh Traders",
            goods_description="Steel Sheets",
            weight="14000 kg",
            freight=21000,
            dalali=350,
            freight_difference=0,
        )

        # 7. "Om Logistics Agency" -- accrues dalali but gets ZERO
        #    payments (tests the empty-state "No records" payments table
        #    with a nonzero balance still showing above it).
        create_bilti(
            "agent_c_unpaid",
            bilti_no=next_no(),
            bilti_date=d(21),
            consignor="Narmada Textiles",
            consignee="Southern Garment Hub",
            vehicle_no="CG04EF7890",
            truck_owner_name="Ramesh Singh Transport",
            agent_name="Om Logistics Agency",
            goods_description="Cotton Yarn Rolls",
            weight="7000 kg",
            freight=12500,
            dalali=500,
            freight_difference=150,
        )

        # 8. All required fields including agent (agent became required per
        #    user feedback #6). Agent set to "Suresh Bhai" to keep ledger
        #    scenarios intact -- see agent_a_* comments above.
        create_bilti(
            "no_extras",
            bilti_no=next_no(),
            bilti_date=d(20),
            consignor="Direct Shipper Co",
            consignee="Direct Receiver Co",
            vehicle_no="MP09XY1235",
            truck_owner_name="Ramesh Singh Transport",
            agent_name="Suresh Bhai",
            goods_description="Furniture",
            weight="3000 kg",
            freight=6000,
        )

        # 9/10. Truck owner "Sagar Roadlines" -- used ONLY in these two
        #    bilties (deliberately not reused elsewhere) so its aggregate
        #    balance is exactly predictable: will be paid EXACTLY the
        #    outstanding total below (tests an exact ₹0.00 balance,
        #    distinct from "no data").
        create_bilti(
            "owner_exact_settle_1",
            bilti_no=next_no(),
            bilti_date=d(26),
            consignor="Ujjain Wholesale Traders",
            consignee="Ratlam Retail Hub",
            vehicle_no="RJ14GB5678",
            truck_owner_name="Sagar Roadlines",
            agent_name="Suresh Bhai",
            goods_description="Packaged Foods",
            weight="4000 kg",
            freight=7000,
            advance_to_owner=2000,
        )
        create_bilti(
            "owner_exact_settle_2",
            bilti_no=next_no(),
            bilti_date=d(23),
            consignor="Ujjain Wholesale Traders",
            consignee="Dewas Retail Hub",
            vehicle_no="RJ14GB5678",
            truck_owner_name="Sagar Roadlines",
            agent_name="Suresh Bhai",
            goods_description="Packaged Foods",
            weight="3500 kg",
            freight=6500,
            advance_to_owner=1500,
        )

        # 11. Truck owner "Gupta Carriers" -- a payment below will be tied
        #    to this specific bilti_id (TruckOwnerPayment.bilti_id), a
        #    field the current UI form doesn't expose a picker for at all.
        create_bilti(
            "owner_payment_linked",
            bilti_no=next_no(),
            bilti_date=d(14),
            consignor="Bhopal Cold Storage",
            consignee="Indore Fresh Mart",
            vehicle_no="UP32AB9999",
            truck_owner_name="Gupta Carriers",
            agent_name="Om Logistics Agency",
            goods_description="Perishable Produce",
            weight="6000 kg",
            freight=9500,
            advance_to_owner=3000,
        )

        # 12. Palti (alternate) vehicle set -- print view's "Palti Vehicle
        #    No." row. Also demonstrates multi-goods-description (newline-
        #    separated lines rendered as separate items on the print GR).
        create_bilti(
            "palti_vehicle",
            bilti_no=next_no(),
            bilti_date=d(13),
            consignor="Highway Spares Ltd",
            consignee="Auto Zone Distributors",
            vehicle_no="MH12CD3456",
            palti_vehicle_no="CG04EF7890",
            truck_owner_name="Bhopal Freight Carriers",
            agent_name="Om Logistics Agency",
            goods_description="Auto Spare Parts\nEngine Components\nGear Assemblies",
            weight="2500 kg",
            freight=5200,
        )

        # 13. Explicitly insured=False (owner's risk) -- print view's
        #    "Not insured / at owner's risk" branch, distinct from the
        #    insured=None (no insurance block at all) case most other
        #    records use.
        create_bilti(
            "explicitly_uninsured",
            bilti_no=next_no(),
            bilti_date=d(12),
            consignor="Budget Movers Co",
            consignee="Low Cost Retail Chain",
            vehicle_no="MP09XY1235",
            truck_owner_name="Ramesh Singh Transport",
            agent_name="Suresh Bhai",
            goods_description="Plastic Goods",
            weight="4200 kg",
            freight=6800,
            insured=False,
        )

        # 14-17. One bilti per GST option, so every checkbox state shows
        #    up somewhere in the seeded data.
        for i, gst in enumerate(["consignor", "consignee", "transporter", "exempted"]):
            create_bilti(
                f"gst_{gst}",
                bilti_no=next_no(),
                bilti_date=d(11 - i),
                consignor=f"GST Test Consignor {gst.title()}",
                consignee=f"GST Test Consignee {gst.title()}",
                vehicle_no=["MP09XY1234", "RJ14GB5678", "GJ05CT4321", "UP32AB9999"][i],
                truck_owner_name="Ramesh Singh Transport",
                agent_name="Suresh Bhai",
                goods_description="Mixed Cargo",
                weight=f"{3000 + i * 500} kg",
                freight=5500 + i * 500,
                gst_paid_by=gst,
            )

        # 18. Large amount -- number formatting/overflow at the upper end
        #    of realistic freight values.
        create_bilti(
            "large_amount",
            bilti_no=next_no(),
            bilti_date=d(10),
            consignor="Bulk Cement Exporters",
            consignee="Coastal Infrastructure Ltd",
            vehicle_no="RJ14GB5678",
            truck_owner_name="Patel Roadways",
            agent_name="Om Logistics Agency",
            goods_description="Cement — Full Truckload",
            weight="18000 kg",
            freight=98750.50,
            dalali=2500,
            freight_difference=800,
            other_charges=450.25,
        )

        # 19. Multi-consignor + multi-goods + weight_per_bag auto-calc demo.
        #    Demonstrates all three features added in the second iteration:
        #    consignor stores newline-separated names, goods_description
        #    stores newline-separated items, weight_per_bag is the per-unit
        #    weight (100 bags × 0.05 MT = 5 MT weight).
        create_bilti(
            "multi_consignor_goods",
            bilti_no=next_no(),
            bilti_date=d(9),
            consignor=(
                "Consolidated Freight & Logistics Solutions Pvt Ltd\n"
                "National Distribution and Warehousing Corp\n"
                "Sunrise Wholesale Mart"
            ),
            consignee="Central Receiving Hub",
            vehicle_no="MH12CD3456",
            truck_owner_name="Bhopal Freight Carriers",
            agent_name="Mahesh Traders",
            goods_description=(
                "Household Plastic Goods\n"
                "Kitchenware Assorted\n"
                "Packaged Consumer Durables\n"
                "Retail-Ready Cartons"
            ),
            package_count="100",
            package_unit="BAG",
            weight_per_bag=0.05,
            weight="5 MT",
            charged_weight="5.2 MT",
            freight_rate=1.8,
            freight=9200,
            dalali=300,
            remark="Multi-consignor consolidated load — verify per-consignor carton count.",
        )

        # 20. Unicode / Hindi party names and goods description -- full
        #    round trip through DB, API, UI, and print/PDF rendering.
        create_bilti(
            "unicode",
            bilti_no=next_no(),
            bilti_date=d(8),
            consignor="श्री गणेश ट्रेडर्स",
            consignee="लक्ष्मी जनरल स्टोर",
            from_location="इंदौर",
            to_location="भोपाल",
            vehicle_no="CG04EF7890",
            truck_owner_name="Ramesh Singh Transport",
            agent_name="Om Logistics Agency",
            goods_description="अनाज की बोरियां (Grain Sacks)",
            weight="4800 किलो",
            freight=7600,
            dalali=250,
            remark="माल सावधानी से उतारें",
        )

        # 21. get-or-create dedup stress: same truck owner as record #2
        #    ("Ramesh Singh Transport"), but with mixed case and stray
        #    whitespace -- must resolve to the SAME truck_owner row, not
        #    create a duplicate. Verify in Admin > Truck Owners: still
        #    only one "Ramesh Singh Transport" row.
        create_bilti(
            "dedup_whitespace_case",
            bilti_no=next_no(),
            bilti_date=d(7),
            consignor="Case Sensitivity Test Co",
            consignee="Whitespace Test Receivers",
            vehicle_no="MP09XY1234",
            truck_owner_name="  ramesh SINGH transport  ",
            agent_name="Suresh Bhai",
            goods_description="Test Cargo",
            weight="2000 kg",
            freight=3500,
        )

        # 22. Linked to a Loading Slip via loading_slip_id -- the full
        #    Loading → Bilti workflow the backend supports end-to-end, but
        #    which BiltiFormDrawer's UI never exposes a picker for today.
        #    No agent here on purpose -- keeps the Mahesh Traders overpaid-
        #    balance scenario below exact (see agent_b_1/2 comment).
        if ls_linked:
            create_bilti(
                "linked_to_loading_slip",
                bilti_no=next_no(),
                bilti_date=d(24),
                loading_slip_id=ls_linked["id"],
                consignor="Ratlam Cement Traders",
                consignee="Ujjain Building Materials",
                vehicle_no="RJ14GB5678",
                truck_owner_name="Patel Roadways",
                agent_name="Mahesh Traders",
                goods_description="Cement Bags",
                weight="9000 kg",
                freight=16200,
            )

        # 23. Same bilti_no as record #1 above, but under a DIFFERENT firm
        #    -- (firm_id, bilti_no) uniqueness is per-firm, not global.
        if firm_2_id:
            create_bilti(
                "cross_firm_same_no",
                bilti_no=f"{MARKER_PREFIX}001",
                bilti_date=d(6),
                firm_id=firm_2_id,
                consignor="Second Firm Test Consignor",
                consignee="Second Firm Test Consignee",
                vehicle_no="MP09XY1234",
                truck_owner_name="Ramesh Singh Transport",
                agent_name="Suresh Bhai",
                goods_description="Firm Isolation Test Cargo",
                weight="1800 kg",
                freight=3100,
            )

        # 24. Soft-delete stress: create, then immediately delete. Must
        #    disappear from every list, search, and ledger everywhere.
        deleted = post(
            client,
            "/api/bilties",
            mk_bilti(
                bilti_no=next_no(),
                bilti_date=d(5),
                consignor="Soft Deleted Consignor",
                consignee="Soft Deleted Consignee",
                vehicle_no="MP09XY1234",
                truck_owner_name="Ramesh Singh Transport",
                agent_name="Suresh Bhai",
                goods_description="This record should not be visible anywhere",
                weight="1000 kg",
                freight=2000,
                dalali=100,
            ),
            label="bilti (soft-delete target)",
        )
        if deleted:
            delete(client, f"/api/bilties/{deleted['id']}", label="soft-delete demo bilti")

        # Bulk out the rest of the page-2 volume with quick variety so the
        # Bilti list crosses its default page-1/limit-20 boundary. No
        # agent_name here on purpose -- attaching "Suresh Bhai" et al.
        # would inflate the exact accrued/balance figures the dedicated
        # agent_a_*/agent_b_* scenarios above are documented against.
        bulk_agents = ["Suresh Bhai", "Om Logistics Agency", "Mahesh Traders"]
        bulk_consignors = ["Narmada Traders", "Vindhya Wholesalers", "Malwa Mills", "Omkareshwar Exports"]
        for i in range(6):
            create_bilti(
                f"bulk_{i}",
                bilti_no=next_no(),
                bilti_date=d(4 - (i % 4)),
                consignor=f"{bulk_consignors[i % 4]} #{i + 1}",
                consignee=f"Bulk Consignee {i + 1}",
                vehicle_no=["MP09XY1234", "RJ14GB5678", "GJ05CT4321", "UP32AB9999"][i % 4],
                truck_owner_name=["Ramesh Singh Transport", "Patel Roadways", "Gupta Carriers"][i % 3],
                agent_name=bulk_agents[i % 3],
                goods_description=["Textiles", "Grain", "Hardware", "Furniture"][i % 4],
                weight=f"{2000 + i * 300} kg",
                freight=4000 + i * 350,
            )

        log(f"Created {len(bilties)} bilties (+1 soft-deleted).")

        # ------------------------------------------------------------------
        # Agent Payments -- three distinct balance scenarios.
        # ------------------------------------------------------------------
        agent_a = bilties.get("agent_a_1", {}).get("agent")  # Suresh Bhai
        agent_b = bilties.get("agent_b_1", {}).get("agent")  # Mahesh Traders

        if agent_a:
            # "Suresh Bhai" also accrues dalali+FD from full_happy_path
            # above -- total accrued here is real (not hand-computed),
            # comfortably more than what's paid below -- normal underpaid
            # balance.
            post(
                client,
                "/api/agent-payments",
                {"firm_id": firm_id, "agent_id": agent_a["id"], "amount": 900, "payment_date": d(15), "mode": "Cash", "remarks": "Partial settlement at month-end"},
                label="agent payment (Suresh Bhai #1)",
            )
            post(
                client,
                "/api/agent-payments",
                {"firm_id": firm_id, "agent_id": agent_a["id"], "amount": 400, "payment_date": d(9), "mode": "UPI"},
                label="agent payment (Suresh Bhai #2, no remarks)",
            )
        if agent_b:
            # "Mahesh Traders" appears ONLY in agent_b_1/2 above (accrued
            # 400+100+350+0=850) -- paid 1200 total here, so this one is
            # exactly OVERPAID: balance goes negative.
            post(
                client,
                "/api/agent-payments",
                {"firm_id": firm_id, "agent_id": agent_b["id"], "amount": 1000, "payment_date": d(16), "mode": "Bank Transfer", "remarks": "Advance against pending business"},
                label="agent payment (Mahesh Traders #1)",
            )
            post(
                client,
                "/api/agent-payments",
                {"firm_id": firm_id, "agent_id": agent_b["id"], "amount": 200, "payment_date": d(5), "mode": "Cheque", "remarks": "Cheque #445218, cleared"},
                label="agent payment (Mahesh Traders #2, overpayment)",
            )
        # "Om Logistics Agency" (agent_c_unpaid) deliberately gets NO
        # payment at all -- empty Recent Payments table with a nonzero
        # balance above it.

        # ------------------------------------------------------------------
        # Truck Owner Payments -- exact settlement, over-receipt-style
        # scenario, a bilti-linked payment, and payment-mode variety.
        # ------------------------------------------------------------------
        owner_settle = bilties.get("owner_exact_settle_1", {}).get("truck_owner")  # Sagar Roadlines
        owner_linked_bilti = bilties.get("owner_payment_linked")  # Gupta Carriers

        if owner_settle:
            # Freight 7000+6500=13500, advance 2000+1500=3500 -> owed 10000.
            # Sagar Roadlines appears nowhere else in this script, so this
            # is exact: pay exactly 10000 -- balance lands on precisely
            # ₹0.00.
            post(
                client,
                "/api/truck-owner-payments",
                {"firm_id": firm_id, "truck_owner_id": owner_settle["id"], "amount": 10000, "payment_date": d(20), "mode": "Bank Transfer", "remarks": "Full and final settlement"},
                label="truck owner payment (Sagar Roadlines, exact settle)",
            )
        if owner_linked_bilti:
            owner_id = owner_linked_bilti["truck_owner"]["id"]
            post(
                client,
                "/api/truck-owner-payments",
                {
                    "firm_id": firm_id,
                    "truck_owner_id": owner_id,
                    "bilti_id": owner_linked_bilti["id"],
                    "amount": 4000,
                    "payment_date": d(13),
                    "mode": "Cash",
                    "remarks": f"Against Bilti {owner_linked_bilti['bilti_no']} specifically",
                },
                label="truck owner payment (Gupta Carriers, bilti-linked)",
            )
            post(
                client,
                "/api/truck-owner-payments",
                {"firm_id": firm_id, "truck_owner_id": owner_id, "amount": 1500, "payment_date": d(3), "mode": "UPI"},
                label="truck owner payment (Gupta Carriers #2)",
            )
        # "Ramesh Singh Transport" accrues freight across many bilties
        # above but gets no payment here -- another unpaid-balance case,
        # this time on the Truck Owner Ledger rather than Agent Ledger.

        # ------------------------------------------------------------------
        # Receipts -- multiple receipts against one bilti, an over-receipt,
        # unicode received_from, and remarks/no-remarks variety.
        # ------------------------------------------------------------------
        full_happy = bilties.get("full_happy_path")
        bare_min = bilties.get("bare_minimum")
        unicode_b = bilties.get("unicode")
        large_b = bilties.get("large_amount")

        if full_happy:
            # Two partial receipts against the SAME bilti, together still
            # under freight -- proves receipts aren't assumed 1:1 with a
            # bilti anywhere in the UI.
            post(client, "/api/receipts", {"firm_id": firm_id, "bilti_id": full_happy["id"], "amount": 8000, "receipt_date": d(20), "received_from": "Ganesh Traders Pvt Ltd", "remarks": "First installment"}, label="receipt (full_happy #1)")
            post(client, "/api/receipts", {"firm_id": firm_id, "bilti_id": full_happy["id"], "amount": 5000, "receipt_date": d(10), "received_from": "Ganesh Traders Pvt Ltd", "remarks": "Second installment"}, label="receipt (full_happy #2)")
        if bare_min:
            # Full settlement in a single receipt, amount == freight.
            post(client, "/api/receipts", {"firm_id": firm_id, "bilti_id": bare_min["id"], "amount": 2200, "receipt_date": d(25), "received_from": "Local Kirana Store"}, label="receipt (bare_minimum, no remarks)")
        if large_b:
            # Over-receipt: total received EXCEEDS freight (98750.50).
            # The backend has no CHECK preventing this -- worth flagging
            # to the user as a possible business-rule gap.
            post(client, "/api/receipts", {"firm_id": firm_id, "bilti_id": large_b["id"], "amount": 90000, "receipt_date": d(6), "received_from": "Bulk Cement Exporters", "remarks": "Advance payment"}, label="receipt (large_amount #1)")
            post(client, "/api/receipts", {"firm_id": firm_id, "bilti_id": large_b["id"], "amount": 15000, "receipt_date": d(2), "received_from": "Bulk Cement Exporters", "remarks": "Final payment -- exceeds invoiced freight, refund pending review"}, label="receipt (large_amount #2, over-receipt)")
        if unicode_b:
            post(client, "/api/receipts", {"firm_id": firm_id, "bilti_id": unicode_b["id"], "amount": 7600, "receipt_date": d(4), "received_from": "श्री गणेश ट्रेडर्स"}, label="receipt (unicode)")

        for tag in ["agent_a_1", "agent_b_1", "owner_exact_settle_2", "gst_consignor", "gst_exempted", "palti_vehicle", "explicitly_uninsured", "no_extras"]:
            b = bilties.get(tag)
            if b:
                post(
                    client,
                    "/api/receipts",
                    {
                        "firm_id": firm_id,
                        "bilti_id": b["id"],
                        "amount": round(float(b["freight"]) * 0.6, 2),
                        "receipt_date": d(2),
                        "received_from": b["consignor"],
                        "remarks": "Partial receipt" if tag != "no_extras" else None,
                    },
                    label=f"receipt ({tag})",
                )

        # ------------------------------------------------------------------
        # Deactivate one vehicle, one agent, one truck owner -- realistic
        # "retired" records that still have historical bilties attached.
        # Admin should show them Inactive; their lookups must drop out of
        # AsyncCombobox (active_only=true) going forward, but ledgers/
        # history for them must still render correctly.
        # ------------------------------------------------------------------
        if agent_b:
            patch(client, f"/api/agents/{agent_b['id']}", {"is_active": False}, label="deactivate Mahesh Traders")
        gst_exempted_bilti = bilties.get("gst_exempted")
        if gst_exempted_bilti:
            vehicle_id = gst_exempted_bilti["vehicle"]["id"]
            patch(client, f"/api/vehicles/{vehicle_id}", {"is_active": False}, label="deactivate a vehicle")
        explicitly_uninsured = bilties.get("explicitly_uninsured")
        if explicitly_uninsured:
            owner_id = explicitly_uninsured["truck_owner"]["id"]
            patch(client, f"/api/truck-owners/{owner_id}", {"is_active": False}, label="deactivate a truck owner")

        log("Demo data seed complete.")


if __name__ == "__main__":
    main()
