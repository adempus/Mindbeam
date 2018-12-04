
Pod::Spec.new do |s|
  s.name         = "RNMindbeamLib"
  s.version      = "1.0.0"
  s.summary      = "RNMindbeamLib"
  s.description  = <<-DESC
                  RNMindbeamLib
                   DESC
  s.homepage     = ""
  s.license      = "MIT"
  # s.license      = { :type => "MIT", :file => "FILE_LICENSE" }
  s.author             = { "author" => "author@domain.cn" }
  s.platform     = :ios, "7.0"
  s.source       = { :git => "https://github.com/author/RNMindbeamLib.git", :tag => "master" }
  s.source_files  = "RNMindbeamLib/**/*.{h,m}"
  s.requires_arc = true


  s.dependency "React"
  #s.dependency "others"

end

  