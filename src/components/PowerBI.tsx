export function PowerBI() {
  return (
    <div
      style={{
        width: "80vw",
        minWidth: "500px",
        height: "90vh",
        maxHeight: "800px",
        paddingBottom: "10px",
      }}
    >
      <iframe
        style={{
          width: "100%",
          height: "100%",
        }}
        src="https://app.powerbi.com/view?r=eyJrIjoiY2NhOWVjMDQtN2E3YS00YzY2LTlhZDctYTc1MDBlY2Y5NmY1IiwidCI6IjI3MWQ1ZTdiLTEzNTAtNGI5Ni1hYjg0LTUyZGJkYTRjZjQwYyIsImMiOjEwfQ%3D%3D"
      ></iframe>
    </div>
  );
}
