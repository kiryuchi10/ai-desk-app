# Frontend Setup (React)

```bash
# Navigate to frontend folder
cd frontend

# Create React app
npx create-react-app .

# Install necessary dependencies
npm install axios react-router-dom

# Start the development server
npm start
```

---

## 📁 Directory Structure

```bash
frontend/
├── src/
│   ├── components/
│   │   ├── ModelSelector.jsx         # Dropdown for OCR/Table/Hybrid mode
│   │   ├── UploadForm.jsx            # Upload file + DPI + extraction trigger
│   │   ├── TablePreview.jsx          # Image preview of table structure
│   │   ├── FeedbackPrompt.jsx        # Prompt user for feedback (Yes/No)
│   │   └── ParentComponent.jsx       # Controls state and orchestrates interaction
│   ├── App.js                        # Entry component mounting ParentComponent
│   ├── index.js                      # Bootstraps React app
│   ├── App.css / index.css          # Styling
```

---

## 🔁 Logical Flow

1. **App.js** mounts `ParentComponent`
2. **ParentComponent.jsx**
   - Manages state for file, mode, DPI, preview image, and feedback
   - Renders: `ModelSelector`, `UploadForm`, `TablePreview`, and `FeedbackPrompt`
3. **ModelSelector.jsx**
   - Lets user select OCR/Table/Hybrid
   - Calls `onSelect(mode)` to update mode in parent
4. **UploadForm.jsx**
   - User uploads PDF, sets DPI, clicks submit
   - Sends file to backend with mode and DPI
   - Receives preview image URL and passes to parent
5. **TablePreview.jsx**
   - Displays preview image received from backend
6. **FeedbackPrompt.jsx**
   - Displays Yes/No buttons asking if output is accurate
   - Sends feedback to backend for logging

---

## 🔧 Notes

- The backend should respond with `{ preview_url: "http://localhost:5000/static/preview_with_grid.png" }`
- All form submission and preview rendering is handled in the browser without Tkinter.
- Preview image can be displayed inside the `TablePreview` component by setting the returned URL as `src`.

This modular structure allows reusability, unit testing, and smooth integration with Flask or FastAPI backend.
