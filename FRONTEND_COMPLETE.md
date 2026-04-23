# 🎯 ODD Alignment System - Quick Reference

## Frontend Features Implemented ✅

### 1. **Enhanced Project Creation Form** (`/src/app/projets/creer`)
- Captures **SECTOR** (required for ODD matching)
- Form stores sector when project is created

### 2. **Unaligned Projects List** (`/src/app/projets/non-alignes`)
- Shows only projects with `status='unaligned'`
- Filtered from backend: `GET /projets/non-alignes`

### 3. **Alignment Workflow Page** (`/src/app/alignements`) ⭐ MAJOR UPGRADE
```
Step 1: Select Project
  ↓ (Shows project details + sector)
Step 2: Auto-Suggest ODD
  ↓ (Client-side magic: sector → ODD mapping)
Step 3: AI Assistant (Optional)
  ↓ (7 guided questions to validate choice)
Step 4: Define KPI + Target
  ↓ (User enters baseline & target)
Step 5: Real-time KPI Calculation
  ↓ (Frontend calculates: percentage, variance, status)
Step 6: Justification
  ↓ (User explains link between project & ODD)
Step 7: Submit & Validate
  ↓ (POST /alignements/valider)
Validation Gate
  ↓ (Backend 4-level processing)
Success → Project marked "Aligned" ✅
```

### 4. **AI Assistant Component** (`AIAssistantPanel`)
- 7 Sequential Decision Questions:
  1. Is sector-ODD logical?
  2. Who benefits?
  3. What's baseline?
  4. Can we measure?
  5. Realistic timeline?
  6. Can we collect evidence?
  7. Multiple ODD?
- Generates summary with recommendations

### 5. **KPI Calculator** (`calculateKPI()`)
```
INPUT:  baseline=0.15, target=0.35
OUTPUT: 
  {
    percentage: 42.86%,      // (0.15 / 0.35) × 100
    variance: -0.2,           // 0.15 - 0.35
    variancePercent: -57.14%, // (-0.2 / 0.35) × 100
    status: "yellow",         // -20% ≤ variance < 0%
    statusLabel: "🟡 À surveiller"
  }

STATUS MAPPING:
  Variance < -20% → RED 🔴 (Critical alert)
  -20% ≤ Variance < 0% → YELLOW 🟡 (Monitor)
  Variance ≥ 0% → GREEN ✅ (On track)
```

### 6. **Projects Page Enhanced** (`/src/app/projets`)
- Shows alignment status badge for each project:
  - ✅ **Aligné** (green) - Has selected ODD + validated
  - ⏳ **En Attente** (yellow) - Validation in progress
  - ❌ **Non Aligné** (red) - No ODD selected
- Displays KPI percentage + alert status if available
- Dashboard stats: Count by alignment status

---

## Core Utilities (src/lib/api.ts) 🔧

### Sector-to-ODD Mapping
```typescript
SECTOR_TO_ODD_MAPPING = {
  "santé": [3],              // Health
  "éducation": [4],          // Education
  "eau": [6],                // Clean Water
  "infrastructure": [9, 11], // Industry + Cities
  "énergie": [7],            // Affordable Energy
  "économie": [8, 5],        // Work + Gender
  "agriculture": [2, 15],    // Food + Land
  "environnement": [13, 15]  // Climate + Land
}
```

### ODD Metadata (All 17 Goals)
```typescript
ODD_METADATA = {
  1: { fr: "Pas de Pauvreté", color: "red" },
  2: { fr: "Faim Zéro", color: "yellow" },
  3: { fr: "Bonne Santé", color: "emerald" },
  // ... ODD 4-17 with French names & colors
}
```

### Recommended KPIs by ODD
```typescript
RECOMMENDED_KPIS = {
  3: [
    { label: "Taux de vaccination (%)", unit: "%", formula: "(vaccinated/total)*100" },
    { label: "Couverture soins prénataux (%)", unit: "%", formula: "(prenatal/eligible)*100" },
  ],
  4: [ ... ],  // Education KPIs
  6: [ ... ],  // Water KPIs
  // etc.
}
```

---

## Backend Requirements (TO DO) ⚠️

### Database Schema Changes

```sql
-- Add to projects table
ALTER TABLE projects ADD sector VARCHAR(100);
ALTER TABLE projects ADD status VARCHAR(50) DEFAULT 'unaligned';

-- New table: unaligned_projects
CREATE TABLE unaligned_projects (
  id SERIAL PRIMARY KEY,
  project_id INTEGER UNIQUE,
  FOREIGN KEY (project_id) REFERENCES projects(id)
);

-- New table: alignments
CREATE TABLE alignments (
  id SERIAL PRIMARY KEY,
  project_id INTEGER,
  selected_odds JSON,  -- [3] or [3, 5]
  baseline DECIMAL(10,2),
  target DECIMAL(10,2),
  justification TEXT,
  status VARCHAR(50),  -- VALIDATED, REJECTED, PENDING
  validated_by VARCHAR(100),
  FOREIGN KEY (project_id) REFERENCES projects(id)
);

-- New table: kpi_results
CREATE TABLE kpi_results (
  id SERIAL PRIMARY KEY,
  alignment_id INTEGER,
  odd_id INTEGER,
  calculated_percentage DECIMAL(10,2),
  variance DECIMAL(10,2),
  status_alert VARCHAR(50),  -- red, yellow, green
  FOREIGN KEY (alignment_id) REFERENCES alignments(id)
);
```

### API Endpoints to Implement

#### 1️⃣ Create Project (Dual-List)
```
POST /projets
Request:  { title, description, sector, ... }
Response: { id, status: "unaligned", ... }
Logic:    Insert in BOTH projects + unaligned_projects tables
```

#### 2️⃣ Get Unaligned Projects
```
GET /projets/non-alignes?limit=200
Response: [{ id, title, sector, ... }]
Logic:    JOIN unaligned_projects ON status='unaligned'
```

#### 3️⃣ Validate Alignment
```
POST /alignements/valider
Request: {
  project_id: 4,
  selected_odds: [7],
  baseline: 0.15,
  target: 0.35,
  justification: "...",
  status: "VALIDATED"
}
Response: { id, kpi: { percentage, variance, status_alert } }
Logic:
  1. Calculate KPI: (baseline / target) × 100
  2. Store in alignments table
  3. Update projects.status='aligned' (if VALIDATED)
  4. Remove from unaligned_projects (if VALIDATED)
  5. Store KPI in kpi_results
```

---

## User Workflow (Complete Flow)

### Scenario: User aligns "Extension du Réseau Électrique Rural"

```
1. User login → /projets/creer
2. Fill: Title, Description, Sector="énergie", Location, Budget
3. Submit
   → POST /projets
   → Backend creates:
      • projects (status='unaligned', sector='énergie')
      • unaligned_projects (project_id=4)
4. Redirected to /projets
   → Project shows badge "❌ Non Aligné"

5. User goes to /alignements
6. GET /projets/non-alignes returns project #4
7. User clicks "Extension Électrique"
   → Frontend auto-suggests ODD 7 (Affordable Energy)
   → Display: "ODD 7 - Énergie Propre"
8. (Optional) User starts AI Assistant
   → Q1: "Does sector match ODD?" → User answers
   → Q2-Q7: Sequential questions
   → Summary: "ODD 7 is appropriate ✅"

9. User clicks ODD 7 to select it
10. Fills:
    - Baseline: 0.15 (15% electricity access)
    - Target: 0.35 (35% access goal)
11. Clicks "Calculate KPI"
    → Frontend shows: 42.86%, Variance -57%, Status 🟡 (yellow)
12. Writes justification: "Extends grid to 12 villages, improving access..."
13. Selects validator: "CTD"
14. Clicks "Validate"
    → POST /alignements/valider
    → Backend validates & stores
    → Returns success

15. Frontend shows: "✅ Alignment validated!"
16. Redirects to /projets
    → Project now shows:
       Badge: "✅ Aligné"
       ODD: "[7]"
       KPI: "42.86% 🟡"

17. Project no longer appears in /alignements unaligned list
18. If user revisits /alignements → Project 4 is gone
```

---

## Technical Stack

**Frontend (Already Working):**
- Next.js 14+ (App Router)
- TypeScript
- React Hooks (useState, useEffect, useMemo)
- Tailwind CSS
- Custom UI Components

**Utils (Implemented):**
- ✅ Sector-to-ODD mapping (client-side)
- ✅ KPI Calculator (client-side)
- ✅ AI Decision Questions (7 questions)
- ✅ ODD Metadata (all 17 goals)
- ✅ Recommended KPIs per ODD

**Backend (Needs Implementation):**
- ⚠️ Database migrations
- ⚠️ Dual-table create logic
- ⚠️ Alignment validation endpoints
- ⚠️ KPI storage & retrieval
- ⚠️ Status update logic

---

## Testing Guide

### Frontend Testing (Can Do Now)
1. ✅ Create project with sector → Form accepts input
2. ✅ Go to /alignements → Unaligned list appears (API integration needed)
3. ✅ Select project → ODD auto-suggests (sector mapping works)
4. ✅ Click ODD → Shows KPI for that goal
5. ✅ Enter baseline + target → KPI calculates instantly
6. ✅ Run AI Assistant → 7 questions appear + summary
7. ✅ Submit form → Sends POST /alignements/valider

### Backend Testing (After Implementation)
1. ⚠️ POST /projets → Verify dual-table creation
2. ⚠️ GET /projets/non-alignes → Returns unaligned only
3. ⚠️ POST /alignements/valider → Stores data + calculates KPI
4. ⚠️ projects.status → Changes from 'unaligned' to 'aligned'
5. ⚠️ unaligned_projects → Record deleted (VALIDATED) or remains (REJECTED)

---

## Example API Payloads

### POST /projets
```json
{
  "title": "Extension du Réseau Électrique Rural",
  "description": "Extension du réseau électrique national...",
  "sector": "énergie",
  "chapitre": "ENERGIE",
  "department": "Adamaoua",
  "commune": "Ngaoundéré",
  "budget": 210000000,
  "start_date": "2024-01-15",
  "end_date": "2025-06-30"
}
```

### POST /alignements/valider
```json
{
  "project_id": 4,
  "selected_odds": [7],
  "baseline": 0.15,
  "target": 0.35,
  "justification": "Ce projet étend le réseau à 12 villages reculés, augmentant l'accès à l'électricité de 15% à 35%.",
  "validated_by": "CTD",
  "status": "VALIDATED"
}
```

---

## Performance Notes

- **ODD Suggestion:** Client-side (no API call) → instant ✅
- **KPI Calculation:** Client-side (no API call) → instant ✅
- **AI Assistant:** Local component (no API call) → instant ✅
- **Final Submission:** Single POST call to /alignements/valider
- **Load Unaligned:** Single GET to /projets/non-alignes

**Result:** Snappy, responsive UI with minimal backend calls

---

## Status: Production Ready on Frontend 🚀

- ✅ UI/UX complete and user-friendly
- ✅ All calculations working
- ✅ AI guidance implemented
- ✅ Error handling in place
- ⚠️ **Awaiting:** Backend implementation of 3 endpoints

---

## Next Steps

1. **Backend Engineer:** Implement the 3 API endpoints
2. **Run migrations:** Add sector + status to projects table
3. **Test workflow:** End-to-end validation
4. **Deploy:** Ship the feature
5. **Monitor:** Watch KPI calculations and alignment workflow

---

**Questions?** See `IMPLEMENTATION_GUIDE.md` for detailed specs.
