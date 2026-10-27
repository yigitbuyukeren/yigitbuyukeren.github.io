// Tek sayfalık CV HTML'ini A4 (595x842 pt) PDF'e çevirir; metin seçilebilir ve ATS okuyucularına açık kalır.
// Kullanım: swift tools/cv/html2pdf.swift girdi.html cikti.pdf
import AppKit
import WebKit

let args = CommandLine.arguments
guard args.count == 3 else { print("kullanım: html2pdf girdi.html cikti.pdf"); exit(2) }
let input = URL(fileURLWithPath: args[1])
let output = URL(fileURLWithPath: args[2])

final class Loader: NSObject, WKNavigationDelegate {
    let web: WKWebView
    init(_ web: WKWebView) { self.web = web }
    func webView(_ w: WKWebView, didFinish navigation: WKNavigation!) {
        // Yazı tipleri otursun diye kısa bekle, taşma kontrolü yap.
        DispatchQueue.main.asyncAfter(deadline: .now() + 0.6) {
            w.evaluateJavaScript("[document.body.scrollHeight, document.body.clientHeight].join(\",\")") { h, _ in
                let parts = ((h as? String) ?? "0,0").split(separator: ",").compactMap { Double($0) }
                let height = parts.first ?? 0, box = parts.last ?? 0
                if height > box + 1 { FileHandle.standardError.write("TAŞMA: içerik \(height) px, sayfa \(box) px\n".data(using: .utf8)!); exit(3) }
                let cfg = WKPDFConfiguration()
                cfg.rect = CGRect(x: 0, y: 0, width: 595, height: 842)
                w.createPDF(configuration: cfg) { result in
                    switch result {
                    case .success(let data):
                        try? data.write(to: output)
                        print("yazıldı: \(output.path) (\(data.count) bayt, içerik \(Int(height)) pt)")
                        exit(0)
                    case .failure(let e):
                        FileHandle.standardError.write("hata: \(e)\n".data(using: .utf8)!); exit(1)
                    }
                }
            }
        }
    }
}

let app = NSApplication.shared
app.setActivationPolicy(.prohibited)
let web = WKWebView(frame: CGRect(x: 0, y: 0, width: 595, height: 842))
let loader = Loader(web)
web.navigationDelegate = loader
web.loadFileURL(input, allowingReadAccessTo: input.deletingLastPathComponent())
app.run()
